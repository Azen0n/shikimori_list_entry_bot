## Telegram bot that allows you to check if user have certain anime in their Shikimori list

### Usage
Sends info message with usage syntax.
```text
/start
```
To use following inline command tag the bot in any chat. While typing anime title you'll see up to ten titles above message that match your input. Select one to check if user have in their anime list.
```text
@shikimori_list_entry_bot Nickname::Anime title
```
Note: Nickname must be exact match of one at [shikimori.one](https://shikimori.one) user profile url.
### Example
```text
@shikimori_list_entry_bot Azenon::Shingeki no Kyojin
```
After selecting title from list you'll send message with "via @" and this result:

![img.png](https://i.imgur.com/bgdMaW5.png)

If the list doesn't appear, make sure that entered nickname and title query is correct, bot is running and `rps` / `rpm` not exceed.