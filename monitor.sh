#!/bin/bash

# Get python install location
python=`which python3 2> /dev/null`
if [ $? -ne 0 ]; then
  python=`which python`
fi
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
  $python main.py "$bot_status" & return_code=$?;pylon_pid=$!
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
      post_msg ${msg_headers[0]} "pylon_factory.py started with pid: $pylon_pid"
      wait "$pylon_pid"; pylon_exit=$?

      # Check return code
      # RC=0 , clean exit
      if [ $pylon_exit -eq 0 ]; then
        post_msg ${msg_headers[0]} "pylon_factory.py exited with RC=$pylon_exit"
        post_msg ${msg_headers[0]} "Script terminating"
        exit 0

      # RC=1 , Uncaught python error, python doesn't give good return codes, so
      # give up, don't even try again, just quit, end it
      elif [ $pylon_exit -eq 1 ]; then
        post_msg ${msg_headers[2]} "pylon_factory.py failed with RC=$pylon_exit"
        post_msg ${msg_headers[2]} "Some uncaught error slipped through"
        exit 1
#         git revert --no-commit HEAD~1
#         git commit -m "AUTO: Reverting to previous commit"; return_code=$?
#         if [ $return_code -eq 0 ]; then
#           git push; return_code=$?
#           if [ $return_code -eq 0 ]; then
#             post_msg ${msg_headers[1]} "Sucessfully reverted, restarting bot"
#             return_code=1
#           else
#             post_msg ${msg_headers[2]} "Unable to push reversion, hep"
#             exit 1
#           fi
#         else
#           post_msg ${msg_headers[2]} "Unable to revert or commit change, hep"
#           exit 1
#         fi

      # RC=2 , clean exit and update
      elif [ $pylon_exit -eq 2 ]; then
        post_msg ${msg_headers[0]} "pylon_factory.py exited with RC=$pylon_exit"
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
        post_msg ${msg_headers[2]} "Unrecognized RC=$pylon_exit, attempting restart"
        bot_status=""
      fi
    fi
done
