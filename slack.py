import logging
logger = logging.getLogger()
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import argparse

# val slackNotify = [String msg |
#     logInfo("sample.rules", "SlackNotify: " + msg);
#     val String url = "https://hooks.slack.com/services/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";
#     val String payload = '{"channel": "#homebot", "username": "HomeBot", "text": "' + msg + '"}';
#     sendHttpPostRequest(url, "application/json", payload);
# ]

#slack_token = os.environ["SLACK_BOT_TOKEN"]
slack_token = "xoxb-280997470256-3854240063347-Q7NQ7HHCPSRF7PNUgTOW5ylD"
slack_default_channel = 'C03QPMD276K'
client = WebClient(token=slack_token)

class Slack:
    def send(channel, message, upload=None):
        if channel is None:
            channel = slack_default_channel

        try:
            if upload is not None:
                response = client.files_upload(
                    channels=channel,
                    file=upload,
                    title=message)
            else:
                response = client.chat_postMessage(
                    channel=channel,
                    text=message
                )
        except SlackApiError as e:
            assert e.response["error"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="Message to send")
    parser.add_argument("--channel", help="Destination channel", default='C03QPMD276K')
    parser.add_argument("--upload", help="File to upload")
    args = parser.parse_args()
    Slack.send(args.channel, args.message, args.upload)