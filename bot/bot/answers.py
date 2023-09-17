
start_text = '''
Hi, fella! I am curly-notifier bot. My purpose is to provide real-time updates on the execution of long-running commands.

To get started, type /help to learn more about how to use me and why I'm useful.
'''


help_text = '''
So, in order to get bash script write /getbashscript. It will give you a function that will send telegram notification when it's done its execution.

An example of usage:
`rwtn "echo hello-world"` - this command will execute echo hello-world and send you something like this __Successfully executed: echo hello-world__
`rwtn "fajlgjdlsjdkf"` - this command will probably send you __Failed to execute: fajlgjdlsjdkf__
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

    curl -X POST -H "Content-Type: application/json" -d "{{
        \\"text\\": \\"$TELEGRAM_NOTIFIER_MESSAGE\\",
        \\"telegram_id\\": \\"{}\\",
        \\"telegram_password\\": \\"{}\\"
    }}" https://{}/send_notification
}}
```
'''
