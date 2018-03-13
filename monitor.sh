#!/bin/bash

msg_headers=("MONITOR" "UPDATE" "ERROR")
return_code=0
retry=0
bot_status="`git log --name-status HEAD^..HEAD`"

# Messaging function
function post_msg {
  printf "%-8s" $1
  echo ": $2"
}

# Bot startup function
function start_bot {
  return_code=0
  python duckbot "$bot_status" & return_code=$?;duck_pid=$!
  # RC!=0 , something bad happened with bash
  if [ $return_code -ne 0 ]; then
    if [ $retry -eq 1 ]; then
      post_msg ${msg_headers[2]} "Unable to start process, hep"
      exit 1
    else
      post_msg ${msg_headers[2]} "Bash failed to start process, retrying"
      retry=1
    fi
  fi
}


# Mainline
while sleep 1; do

    # Attempt to start bot
    start_bot

    if [ $return_code -eq 0 ]; then
      retry=0
      # Wait for finish and grab return code
      post_msg ${msg_headers[0]} "duckbot started with pid: $duck_pid"
      wait "$duck_pid"; duck_exit=$?

      # Check return code
      # RC=0 , clean exit
      if [ $duck_exit -eq 0 ]; then
        post_msg ${msg_headers[0]} "duckbot exited with RC=$duck_exit"
        post_msg ${msg_headers[0]} "Script terminating"
        exit 0

      # RC=1 , Uncaught python error, python doesn't give good return codes, so
      # give up, don't even try again, just quit, end it
      elif [ $duck_exit -eq 1 ]; then
        post_msg ${msg_headers[2]} "duckbot failed with RC=$duck_exit"
        post_msg ${msg_headers[2]} "Some uncaught error slipped through"
        exit 1

      # RC=2 , clean exit and update
      elif [ $duck_exit -eq 2 ]; then
        post_msg ${msg_headers[0]} "duckbot exited with RC=$duck_exit"
        post_msg ${msg_headers[1]} "Beginning update"
        git pull; return_code=$?

        if [ $return_code -eq 0 ]; then
          post_msg ${msg_headers[1]} "Pull successful, restarting bot with new code"
          bot_status="`git log --name-status HEAD^..HEAD`"
        else
          post_msg ${msg_headers[2]} "Pull unsuccessful, restarting bot with old code"
          bot_status="`git log --name-status HEAD^..HEAD`"
        fi

      # RC=? , unknown return code from bot, attempt to restart
      else
        post_msg ${msg_headers[2]} "Unrecognized RC=$duck_exit, attempting restart"
        bot_status=""
      fi
    fi
done
