# Discord_HAQQ_Proposals_Bot

ИНСТРУКЦИЯ НАСТРОЙКИ БОТА 

1. Добавьте сервер в дискорде
2. Перейдите в раздел APP SETTINGS, на вкладку Advanced и переместите селектор Developer mode — режим разработчика активируется
3. На вкладке Applications выберите New Application на портале разработчиков Discord (https://discord.com/developers/applications)
4. Перейдите на вкладку Bot и нажмите Add Bot, чтобы добавить нового бота
5. На вкладке Bot отобразится вся информация о нем. Тут можно изменить его имя, добавить изображение и скопировать токен бота. Этот токен понадобится вам для настройки модуля Discord
6. Теперь перейдите на вкладку OAuth2 — тут можно настроить разрешения и получить ссылку на вашего бота
7. Вставьте скопированную ссылку в адресную строку браузера и перейдите по ней — откроется окошко вашего приложения. Выберите ваш сервер в раскрывающемся списке и нажмите Continue
9. Вставьте свой токен в строку 39
10. Если вы не используете веб-сервер, такой как Repl.it , для размещения своего бота, вам нужно будет создать файл env , содержащий ваш токен, и изменить строку 39 в client.run(os.getenv("TOKEN"))
11. Версия Discord Bot собирает данные в чат сервера Discord, бот будет пинговать только новые голосование после их проверки в соответствии с определенными временными рамками, которые можно настроить в строке 36
