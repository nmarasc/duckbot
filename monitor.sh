#!/bin/bash

# Last Updated: 2.2
# For diag code documentation see diagCodes.py

running=1
return_code=0
retry=0
duck_parms=$@

# Bot startup function
function start_bot {
  return_code=0
  python duckbot/main.py $duck_parms & return_code=$?;duck_pid=$!
  # RC!=0 , something bad happened with bash
  if [ $return_code -ne 0 ]; then
    if [ $retry -gt 0 ]; then
      echo "MON0031E" "Unable to start process, hep"
      running=0
    else
      echo "MON0030E" "Bash failed to start process, retrying"
      retry=$((retry+1))
    fi
  fi
}

# Check for compile time syntax errors,
# not to be confused with runtime syntax errors
function syntax_check {
  return_code=0
  python syntax_check.py; return_code=$?
  if [ $return_code -ne 0 ]; then
    echo "MON0040E" "Code failed syntax check"
    running=0
    # Possibly put git restore here later
  # Else clean up compiled files?
  fi
}

# Mainline
syntax_check
while [ $running -eq 1 ]; do

    # Attempt to start bot
    start_bot

    if [ $return_code -eq 0 ]; then
      retry=0
      # Wait for finish and grab return code
      echo "MON0000I" "Duckbot started with pid=$duck_pid"
      export set DUCK_PID=$duck_pid
      wait "$duck_pid"; duck_exit=$?
      echo "MON0010I" "Duckbot exited with RC=$duck_exit"

      # Check return code
      # RC=0 , clean exit
      if [ $duck_exit -eq 0 ]; then
        echo "Shutting down..."
        return_code=$duck_exit
        running=0

      # RC=1 , Uncaught python error, python doesn't give good return codes
      elif [ $duck_exit -eq 1 ]; then
        echo "MON0011E" "Uncaught Python error, possible bad build"
        return_code=$duck_exit
        running=0

      # RC=2 , clean exit and update
      elif [ $duck_exit -eq 2 ]; then
        echo "MON0012I" "Update signal received"
        echo "MON0020I" "Starting bot update"
        git pull; return_code=$?

        if [ $return_code -eq 0 ]; then
          echo "MON0021I" "Pull successful, check and restart"
          syntax_check
        else
          echo "MON0021E" "Pull unsuccessful, restarting bot with old code"
        fi

      # RC=20 , rtm_read generic error , restart bot for now
      elif [ $duck_exit -eq 20]; then
        echo "MON0013E" "rtm_read generic error, restarting bot"

      # RC=21 , timeout error on rtm_read, restart bot
      elif [ $duck_exit -eq 21]; then
        echo "MON0014E" "rmt_read timeout error, restarting bot"

      # RC=? , unknown return code from bot, attempt to restart
      else
        echo "MON0019E" "Unhandled RC, attempting restart"
        return_code=$duck_exit
        running=0
      fi
    fi
done
(exit $return_code)
