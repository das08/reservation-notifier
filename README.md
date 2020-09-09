# reservation-notifier
教習所の技能予約の空きを通知するシステムです

## できること
- 🌸前回実行時の予約空き状況との差分を表示
- 🔔設定した日数以内の空き状況をLineで通知
- 📗設定した予約希望日リストの予約が取れる場合、自動的に予約

## 実行方法
`.env_sample`を参考に同じディレクトリ内に`.env`を作成します。  

次に`main.py`をCronで定期実行します。  

```bash
#[cron.sh]
#!/bin/sh
python /home/das08/reservation-notifier/main.py
```

```bash
*/30 0-16,23 * * * /home/das08/reservation-notifier/cron.sh >> /home/das08/reservation-notifier/.log 2>&1
```

（30分おきに空きを確認するようにしています）

## スクリーンショット
<img width="360" alt="スクリーンショット 2020-09-09 22 40 58" src="https://user-images.githubusercontent.com/41512077/92606122-9178b780-f2ed-11ea-8282-bbbdf22b8ada.png">
