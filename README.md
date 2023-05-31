# Slack Feiertagsbot

Posted die nächsten ansehehden Feiertage in einen Slack Channel im folgenden Format:
```md
*Anstehende Feiertage:*
<Emoji> <Feiertag Name> am <Tag Name>, <DD.MM.YYYY>
```

## Umgebungsvariablen
- `SLACK_CHANNEL`: (default: `holiday-test`) Name des Slack Channels
- `SLACK_TOKEN`: Slack App Token
- `SEARCH_WEEKS`: (default: `2`) Anzahl der kommenden Wochen, in denen gesucht werden soll