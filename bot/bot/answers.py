
start_text = '''
* Well, you started conversation *
'''


help_text = '''
* Well, this is definately a bot and it has purpose i suppose *
'''


bash_script = '''
Add this function in your .whateverrc file

```
# run with telegram notification
function rwtn {{
    local cmd="$1"

    ( 
        set -e
        eval "$cmd" 
    )

    if [ $? -eq 0 ]; then
        TELEGRAM_NOTIFIER_MESSAGE="Successfully executed: $cmd"
        echo "Successfully executed: $cmd"
    else
        TELEGRAM_NOTIFIER_MESSAGE="Failed to execute: $cmd"
        echo "Failed to execute: $cmd"
    fi

    curl -X POST -H "Content-Type: application/json" -d '{{
        "text": $TELEGRAM_NOTIFIER_MESSAGE,
        "telegram_id": {},
        "telegram_password": {}
    }}' http://{}/send_notification
}}
```
'''