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
- `STATE`: (default: `NATIONAL`) Gibt an, für welche Region/Bundesland Feiertage gesucht werden sollen (siehe Tabelle unten)

## Bundesländer Übersicht

Aus der Tabelle kann ein Wert für die Umgebungsvariable `STATE` gewählt werden.

| Wert      	 | Beschreibung        	    |
|-------------|----------------------------|
| ALL      	  | Alle Feiertage         	 |
| NATIONAL 	  | Nationale Feiertage    	 |
| BW       	  | Baden-Württemberg      	 |
| BY       	  | Bayern                 	 |
| BE       	  | Berlin                 	 |
| BB       	  | Brandenburg            	 |
| HB       	  | Bremen                 	 |
| HH       	  | Hamburg                	 |
| HE       	  | Hessen                 	 |
| MV       	  | Mecklenburg-Vorpommern 	 |
| NI       	  | Niedersachsen          	 |
| NW       	  | Nordrhein-Westfalen    	 |
| RP       	  | Rheinland-Pfalz        	 |
| SL       	  | Saarland               	 |
| SN       	  | Sachsen                	 |
| ST       	  | Sachsen-Anhalt         	 |
| SH       	  | Schleswig-Holstein     	 |
| TH       	  | Thüringen              	 |