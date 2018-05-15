#!/bin/bash

# For diag code documentation see diagCodes.py

return_code=0
retry=0

# Bot startup function
function start_bot {
  return_code=0
  python bot/main.py & return_code=$?;duck_pid=$!
  # RC!=0 , something bad happened with bash
  if [ $return_code -ne 0 ]; then
    if [ $retry -eq 1 ]; then
      echo "MON0001E" "Unable to start process, hep"
      exit 1
    else
      echo "MON0000E" "Bash failed to start process, retrying"
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
    echo "MON0010E" "Code failed syntax check"
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
      echo "MON0000I" "duckbot started with pid: $duck_pid"
      wait "$duck_pid"; duck_exit=$?

      # Check return code
      # RC=0 , clean exit
      if [ $duck_exit -eq 0 ]; then
        echo "MON0010I" "duckbot exited, RC=$duck_exit"
        exit 0

      # RC=1 , Uncaught python error, python doesn't give good return codes
      elif [ $duck_exit -eq 1 ]; then
        echo "MON0020E" "duckbot failed, RC=$duck_exit, python error"
        exit 1

      # RC=2 , clean exit and update
      elif [ $duck_exit -eq 2 ]; then
        echo ${inf_codes[3]} "duckbot exited, RC=$duck_exit, starting update"
        git pull; return_code=$?

        if [ $return_code -eq 0 ]; then
          echo ${inf_codes[5]} "Pull successful, checking new code"
          syntax_check
        else
          echo ${err_codes[4]} "Pull unsuccessful, restarting bot with old code"
        fi

      # RC=20 , rtm_read generic error , restart bot for now
      elif [ $duck_exit -eq 20]; then
        echo ${err_codes[5]} "duckbot failed with RC=$duck_exit"
        echo ${err_codes[6]} "rtm_read generic error, restarting bot"

      # RC=21 , timeout error on rtm_read, restart bot
      elif [ $duck_exit -eq 21]; then
        echo ${err_codes[7]} "duckbot failed with RC=$duck_exit"
        echo ${err_codes[8]} "rmt_read timeout error, restarting bot"

      # RC=? , unknown return code from bot, attempt to restart
      else
        echo ${err_codes[9]} "Unrecognized RC=$duck_exit, attempting restart"
      fi
    fi
done
