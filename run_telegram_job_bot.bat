@echo off
title Telegram Job Notification Bot (@rabi_job_bot)
cd /d "%~dp0"
echo ======================================================================
echo Launching Telegram Job Notifier Service for @rabi_job_bot
echo Daily Report Time: 09:00 AM
echo Commands: /report, /sent, /pending, /followups, /help
echo ======================================================================
python telegram_job_notifier.py
pause
