#!/bin/bash

msg_headers=("MONITOR" "UPDATE" "ERROR")
return_code=0
retry=0

# Messaging function
function post_msg {
  printf "%-8s" $1
  echo ": $2"
}

# Bot startup function
function start_bot {
  return_code=0
  python bot/main.py & return_code=$?;duck_pid=$!
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

# Check for compile time syntax errors,
# not to be confused with runtime syntax errors
function syntax_check {
  return_code=0
  python syntax_check.py; return_code=$?
  if [ $return_code -ne 0 ]; then
    post_msg ${msg_headers[2]} "Code failed syntax check"
    # Possibly put git restore here later
    exit 2
  # Else clean up compiled files?
  fi
}

# Mainline
syntax_check
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

      # RC=1 , Uncaught python error, python doesn't give good return codes
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
          post_msg ${msg_headers[1]} "Pull successful, checking new code"
          syntax_check
        else
          post_msg ${msg_headers[2]} "Pull unsuccessful, restarting bot with old code"
        fi

      # RC=20 , rtm_read generic error , restart bot for now
      elif [ $duck_exit -eq 20]; then
        post_msg ${msg_headers[2]} "duckbot failed with RC=$duck_exit"
        post_msg ${msg_headers[2]} "rtm_read generic error, restarting bot"

      # RC=21 , timeout error on rtm_read, restart bot
      elif [ $duck_exit -eq 21]; then
        post_msg ${msg_headers[2]} "duckbot failed with RC=$duck_exit"
        post_msg ${msg_headers[2]} "rmt_read timeout error, restarting bot"

      # RC=? , unknown return code from bot, attempt to restart
      else
        post_msg ${msg_headers[2]} "Unrecognized RC=$duck_exit, attempting restart"
      fi
    fi
done
