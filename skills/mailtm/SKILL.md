---
name: mailtm
description: Temporary email via mail.tm for testing sign-up flows, OTPs, and email verification.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
  tags: "email,temp,testing,mailtm"
---

<skill name="mailtm">

<when_to_use>
- Пользователь просит временный / disposable email.
- Пользователь говорит про регистрацию, тестирование email-воркфлоу, OTP, подтверждение почты.
- Пользователь напрямую упоминает "mailtm" или "mail.tm".
</when_to_use>

<context>
Модуль mailtm_agent находится в ./src директории этого скилла.
Используй хелпер-скрипт mailtm.py для всех операций.
</context>

<capabilities>
- Создавать временные email-адреса через mail.tm
- Повторно использовать ранее созданный inbox в рамках сессии
- Периодически опрашивать inbox и получать новые письма
- Парсить HTML-тело письма в обычный текст
- Находить и явно выписывать коды подтверждения и ссылки
- Скачивать вложения писем на диск
</capabilities>

<behavior>

<critical>
ВСЕГДА используй хелпер-скрипт mailtm.py вместо inline Python.
Путь к скрипту: ~/.config/opencode/skills/mailtm/mailtm.py

Команды:
- `python ~/.config/opencode/skills/mailtm/mailtm.py address` - показать текущий email
- `python ~/.config/opencode/skills/mailtm/mailtm.py list` - список писем
- `python ~/.config/opencode/skills/mailtm/mailtm.py wait` - ждать новое письмо (90 сек)
- `python ~/.config/opencode/skills/mailtm/mailtm.py read <id>` - прочитать письмо
- `python ~/.config/opencode/skills/mailtm/mailtm.py new` - создать новый inbox
</critical>

<output_format>
КРИТИЧНО: Скрипт mailtm.py уже форматирует вывод. НЕ ДУБЛИРУЙ результат!
- После выполнения команды НЕ переписывай/не переформатируй вывод скрипта
- Просто подтверди действие одной короткой фразой если нужно
- Если нужно выделить что-то важное (код, ссылку) — укажи только это
</output_format>

<step priority="high">
Если пользователь просит временный email:
1. Запусти: `python ~/.config/opencode/skills/mailtm/mailtm.py address`
2. НЕ дублируй вывод — он уже показан
</step>

<step>
Если пользователь ждёт письмо:
1. Запусти: `python ~/.config/opencode/skills/mailtm/mailtm.py wait`
2. НЕ дублируй — если есть код/ссылка, укажи только их отдельно
</step>

<step>
Если пользователь просит список/содержимое писем:
1. Запусти соответствующую команду
2. НЕ дублируй вывод скрипта
</step>

<step>
Если пользователь просит новый inbox:
1. Запусти: `python ~/.config/opencode/skills/mailtm/mailtm.py new`
2. НЕ дублируй — адрес уже показан
</step>

<step>
Никогда не используй mail.tm для чувствительных или продакшн-учёток.
</step>

</behavior>

</skill>
