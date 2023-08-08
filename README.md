# Slack Feiertagsbot

Benachrichtigt über die anstehenden, deutschen Feiertage in einen Slack Channel im folgenden Format:
```md
*Anstehende Feiertage:*
<Emoji> *<Bundesland>* | *<Feiertag Name>* am <Tag Name>, <DD.MM.YYYY>
> <optionaler Hinweis>
```

## Umgebungsvariablen
- `SLACK_CHANNEL`: Name des Slack Channels
- `SLACK_TOKEN`: Slack App Token
- `SEARCH_WEEKS`: (default: `2`) Anzahl der kommenden Wochen, in denen gesucht werden soll
- `STATE`: (default: `ALL`) Gibt an, für welche Region/Bundesland Feiertage gesucht werden sollen (siehe [Tabelle unten](#bundesländer-übersicht))

## Bundesländer Übersicht

Aus der Tabelle kann ein Wert für die Umgebungsvariable `STATE` gewählt werden.

| Wert      	 | Beschreibung        	                    |
|-------------|------------------------------------------|
| ALL      	  | Alle Feiertage         	                 |
| NATIONAL 	  | Deutschland (Nur Nationalfeiertage)    	 |
| BW       	  | Baden-Württemberg      	                 |
| BY       	  | Bayern                 	                 |
| BE       	  | Berlin                 	                 |
| BB       	  | Brandenburg            	                 |
| HB       	  | Bremen                 	                 |
| HH       	  | Hamburg                	                 |
| HE       	  | Hessen                 	                 |
| MV       	  | Mecklenburg-Vorpommern 	                 |
| NI       	  | Niedersachsen          	                 |
| NW       	  | Nordrhein-Westfalen    	                 |
| RP       	  | Rheinland-Pfalz        	                 |
| SL       	  | Saarland               	                 |
| SN       	  | Sachsen                	                 |
| ST       	  | Sachsen-Anhalt         	                 |
| SH       	  | Schleswig-Holstein     	                 |
| TH       	  | Thüringen              	                 |
