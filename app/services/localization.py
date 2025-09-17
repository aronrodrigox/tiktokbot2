from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Literal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Типы языков
Language = Literal["ru", "en", "ar", "es", "fr", "de", "pt", "ja", "pl", "tr"]

# Переводы
TRANSLATIONS: Dict[Language, Dict[str, str]] = {
    "ru": {
        # Стартовое сообщение
        "start_private": (
            "👋 Привет! Я помогу скачать видео из TikTok без водяного знака! 🚀\n\n"
            "📎 Отправь ссылку на видео TikTok, и я верну файл без водяного знака! ✨\n\n"
            "💡 Можешь добавить меня в чат для удобного использования! 😊\n\n"
            "🌐 Используй /lang для смены языка"
        ),
        "start_group": (
            "🎉 Привет, {chat_title}! 👋\n\n"
            "🤖 Я бот для скачивания видео из TikTok без водяного знака! 🚀\n\n"
            "📎 Просто отправь ссылку на видео TikTok, и я верну файл без водяного знака! ✨\n\n"
            "⚠️ Для работы в чате мне нужны права администратора! 👑\n\n"
            "💡 Работаю быстро и качественно! 😊\n\n"
            "🌐 Используй /lang для смены языка"
        ),
        "add_to_chat": "➕ Добавить в чат",
        
        # Ошибки
        "invalid_link": (
            "❌ Некорректная ссылка Тик Ток.\n\n"
            "Для загрузки видео, отправьте ссылку в формате:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Не удалось получить видео. Проверь ссылку или попробуй позже.",
        "service_unavailable": "🔧 Сервис временно недоступен. Ищем стабильный API...",
        "invalid_video_url": "❌ Получен некорректный URL видео. Попробуй другую ссылку.",
        
        # Прогресс
        "progress_start": "⏳ Начинаем загрузку...",
        "progress_analyzing": "🔍 Анализируем ссылку...",
        "progress_getting": "🎥 Получаем видео...",
        "progress_downloading": "📥 Скачиваем файл...",
        "progress_sending": "📤 Отправляем видео...",
        
        # Подпись видео
        "video_caption": "Скачано с помощью: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Выберите язык / Choose language:",
        "language_changed": "✅ Язык изменен на русский",
        "current_language": "🇷🇺 Русский",
        
        # Админ команды
        "logs_enabled": "Логи включены ✅",
        "logs_disabled": "Логи выключены 🚫",
        "cache_cleared": "🧹 Кэш очищен!\nБыло записей: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Создание рассылки</b>\n\n"
            "👥 Пользователей в базе: <b>{user_count}</b>\n\n"
            "Отправьте любое сообщение для рассылки:\n"
            "• 📝 Текст\n"
            "• 🖼️ Изображение\n"
            "• 📹 Видео\n"
            "• 📄 Документ\n"
            "• 🎵 Аудио"
        ),
        "broadcast_no_users": "❌ Нет пользователей для рассылки",
        "broadcast_confirm": (
            "📢 <b>Подтверждение рассылки</b>\n\n"
            "👥 Получателей: <b>{user_count}</b>\n"
            "📝 Тип: {message_type}\n\n"
            "Нажмите 'Отправить рассылку' для подтверждения:"
        ),
        "broadcast_send": "✅ Отправить рассылку",
        "broadcast_cancel": "❌ Отменить",
        "broadcast_preview": "👁️ Предпросмотр",
        "broadcast_stats": "📊 Статистика пользователей",
        "broadcast_sending": "📤 Отправка рассылки...",
        "broadcast_completed": (
            "📢 <b>Рассылка завершена!</b>\n\n"
            "✅ Успешно отправлено: <b>{success_count}</b>\n"
            "❌ Ошибок: <b>{error_count}</b>\n"
            "👥 Всего получателей: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Рассылка отменена.",
        "broadcast_reset": "✅ Состояние рассылки сброшено",
        "broadcast_no_state": "ℹ️ Нет активного состояния рассылки",
        "broadcast_preview_text": "👁️ <b>Предпросмотр рассылки:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Текст",
        "message_type_photo": "🖼️ Изображение",
        "message_type_video": "📹 Видео",
        "message_type_document": "📄 Документ",
        "message_type_audio": "🎵 Аудио",
    },
    
    "en": {
        # Стартовое сообщение
        "start_private": (
            "👋 Hello! I'll help you download TikTok videos without watermarks! 🚀\n\n"
            "📎 Send a TikTok video link and I'll return the file without watermark! ✨\n\n"
            "💡 You can add me to a chat for convenient use! 😊\n\n"
            "🌐 Use /lang to change language"
        ),
        "start_group": (
            "🎉 Hello, {chat_title}! 👋\n\n"
            "🤖 I'm a bot for downloading TikTok videos without watermarks! 🚀\n\n"
            "📎 Just send a TikTok video link and I'll return the file without watermark! ✨\n\n"
            "⚠️ I need admin rights to work in the chat! 👑\n\n"
            "💡 I work fast and efficiently! 😊\n\n"
            "🌐 Use /lang to change language"
        ),
        "add_to_chat": "➕ Add to chat",
        
        # Ошибки
        "invalid_link": (
            "❌ Invalid TikTok link.\n\n"
            "To download video, send a link in format:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Failed to get video. Check the link or try later.",
        "service_unavailable": "🔧 Service temporarily unavailable. Looking for stable API...",
        "invalid_video_url": "❌ Received invalid video URL. Try another link.",
        
        # Прогресс
        "progress_start": "⏳ Starting download...",
        "progress_analyzing": "🔍 Analyzing link...",
        "progress_getting": "🎥 Getting video...",
        "progress_downloading": "📥 Downloading file...",
        "progress_sending": "📤 Sending video...",
        
        # Подпись видео
        "video_caption": "Downloaded with: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Choose language / Выберите язык:",
        "language_changed": "✅ Language changed to English",
        "current_language": "🇺🇸 English",
        
        # Админ команды
        "logs_enabled": "Logs enabled ✅",
        "logs_disabled": "Logs disabled 🚫",
        "cache_cleared": "🧹 Cache cleared!\nRecords: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Creating broadcast</b>\n\n"
            "👥 Users in database: <b>{user_count}</b>\n\n"
            "Send any message for broadcast:\n"
            "• 📝 Text\n"
            "• 🖼️ Image\n"
            "• 📹 Video\n"
            "• 📄 Document\n"
            "• 🎵 Audio"
        ),
        "broadcast_no_users": "❌ No users for broadcast",
        "broadcast_confirm": (
            "📢 <b>Broadcast confirmation</b>\n\n"
            "👥 Recipients: <b>{user_count}</b>\n"
            "📝 Type: {message_type}\n\n"
            "Click 'Send broadcast' to confirm:"
        ),
        "broadcast_send": "✅ Send broadcast",
        "broadcast_cancel": "❌ Cancel",
        "broadcast_preview": "👁️ Preview",
        "broadcast_stats": "📊 User statistics",
        "broadcast_sending": "📤 Sending broadcast...",
        "broadcast_completed": (
            "📢 <b>Broadcast completed!</b>\n\n"
            "✅ Successfully sent: <b>{success_count}</b>\n"
            "❌ Errors: <b>{error_count}</b>\n"
            "👥 Total recipients: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Broadcast cancelled.",
        "broadcast_reset": "✅ Broadcast state reset",
        "broadcast_no_state": "ℹ️ No active broadcast state",
        "broadcast_preview_text": "👁️ <b>Broadcast preview:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Text",
        "message_type_photo": "🖼️ Image",
        "message_type_video": "📹 Video",
        "message_type_document": "📄 Document",
        "message_type_audio": "🎵 Audio",
    },
    
    "ar": {
        # Стартовое сообщение
        "start_private": (
            "👋 مرحباً! سأساعدك في تحميل مقاطع فيديو TikTok بدون علامة مائية! 🚀\n\n"
            "📎 أرسل رابط فيديو TikTok وسأعيد لك الملف بدون علامة مائية! ✨\n\n"
            "💡 يمكنك إضافتي إلى محادثة للاستخدام المريح! 😊\n\n"
            "🌐 استخدم /lang لتغيير اللغة"
        ),
        "start_group": (
            "🎉 مرحباً، {chat_title}! 👋\n\n"
            "🤖 أنا بوت لتحميل مقاطع فيديو TikTok بدون علامة مائية! 🚀\n\n"
            "📎 فقط أرسل رابط فيديو TikTok وسأعيد لك الملف بدون علامة مائية! ✨\n\n"
            "⚠️ أحتاج صلاحيات المدير للعمل في المحادثة! 👑\n\n"
            "💡 أعمل بسرعة وكفاءة! 😊\n\n"
            "🌐 استخدم /lang لتغيير اللغة"
        ),
        "add_to_chat": "➕ إضافة إلى المحادثة",
        
        # Ошибки
        "invalid_link": (
            "❌ رابط TikTok غير صحيح.\n\n"
            "لتحميل الفيديو، أرسل رابط بالتنسيق:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ فشل في الحصول على الفيديو. تحقق من الرابط أو حاول لاحقاً.",
        "service_unavailable": "🔧 الخدمة غير متاحة مؤقتاً. نبحث عن API مستقر...",
        "invalid_video_url": "❌ تم استلام رابط فيديو غير صحيح. جرب رابط آخر.",
        
        # Прогресс
        "progress_start": "⏳ بدء التحميل...",
        "progress_analyzing": "🔍 تحليل الرابط...",
        "progress_getting": "🎥 الحصول على الفيديو...",
        "progress_downloading": "📥 تحميل الملف...",
        "progress_sending": "📤 إرسال الفيديو...",
        
        # Подпись видео
        "video_caption": "تم التحميل بواسطة: @{bot_username}",
        
        # Языки
        "language_select": "🌐 اختر اللغة / Choose language / Выберите язык:",
        "language_changed": "✅ تم تغيير اللغة إلى العربية",
        "current_language": "🇸🇦 العربية",
        
        # Админ команды
        "logs_enabled": "تم تفعيل السجلات ✅",
        "logs_disabled": "تم إيقاف السجلات 🚫",
        "cache_cleared": "🧹 تم مسح الذاكرة المؤقتة!\nالسجلات: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>إنشاء إرسال جماعي</b>\n\n"
            "👥 المستخدمون في قاعدة البيانات: <b>{user_count}</b>\n\n"
            "أرسل أي رسالة للإرسال الجماعي:\n"
            "• 📝 نص\n"
            "• 🖼️ صورة\n"
            "• 📹 فيديو\n"
            "• 📄 مستند\n"
            "• 🎵 صوت"
        ),
        "broadcast_no_users": "❌ لا يوجد مستخدمون للإرسال الجماعي",
        "broadcast_confirm": (
            "📢 <b>تأكيد الإرسال الجماعي</b>\n\n"
            "👥 المستلمون: <b>{user_count}</b>\n"
            "📝 النوع: {message_type}\n\n"
            "اضغط 'إرسال الإرسال الجماعي' للتأكيد:"
        ),
        "broadcast_send": "✅ إرسال الإرسال الجماعي",
        "broadcast_cancel": "❌ إلغاء",
        "broadcast_preview": "👁️ معاينة",
        "broadcast_stats": "📊 إحصائيات المستخدمين",
        "broadcast_sending": "📤 إرسال الإرسال الجماعي...",
        "broadcast_completed": (
            "📢 <b>تم الإرسال الجماعي!</b>\n\n"
            "✅ تم الإرسال بنجاح: <b>{success_count}</b>\n"
            "❌ أخطاء: <b>{error_count}</b>\n"
            "👥 إجمالي المستلمين: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ تم إلغاء الإرسال الجماعي.",
        "broadcast_reset": "✅ تم إعادة تعيين حالة الإرسال الجماعي",
        "broadcast_no_state": "ℹ️ لا توجد حالة إرسال جماعي نشطة",
        "broadcast_preview_text": "👁️ <b>معاينة الإرسال الجماعي:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 نص",
        "message_type_photo": "🖼️ صورة",
        "message_type_video": "📹 فيديو",
        "message_type_document": "📄 مستند",
        "message_type_audio": "🎵 صوت",
    },
    
    "es": {
        # Стартовое сообщение
        "start_private": (
            "👋 ¡Hola! ¡Te ayudo a descargar videos de TikTok sin marca de agua! 🚀\n\n"
            "📎 ¡Envía un enlace de video de TikTok y te devolveré el archivo sin marca de agua! ✨\n\n"
            "💡 ¡Puedes agregarme a un chat para uso conveniente! 😊\n\n"
            "🌐 Usa /lang para cambiar idioma"
        ),
        "start_group": (
            "🎉 ¡Hola, {chat_title}! 👋\n\n"
            "🤖 ¡Soy un bot para descargar videos de TikTok sin marca de agua! 🚀\n\n"
            "📎 ¡Solo envía un enlace de video de TikTok y te devolveré el archivo sin marca de agua! ✨\n\n"
            "⚠️ ¡Necesito permisos de administrador para trabajar en el chat! 👑\n\n"
            "💡 ¡Trabajo rápido y eficientemente! 😊\n\n"
            "🌐 Usa /lang para cambiar idioma"
        ),
        "add_to_chat": "➕ Agregar al chat",
        
        # Ошибки
        "invalid_link": (
            "❌ Enlace de TikTok inválido.\n\n"
            "Para descargar video, envía un enlace en formato:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ No se pudo obtener el video. Verifica el enlace o intenta más tarde.",
        "service_unavailable": "🔧 Servicio temporalmente no disponible. Buscando API estable...",
        "invalid_video_url": "❌ Se recibió una URL de video inválida. Prueba otro enlace.",
        
        # Прогресс
        "progress_start": "⏳ Iniciando descarga...",
        "progress_analyzing": "🔍 Analizando enlace...",
        "progress_getting": "🎥 Obteniendo video...",
        "progress_downloading": "📥 Descargando archivo...",
        "progress_sending": "📤 Enviando video...",
        
        # Подпись видео
        "video_caption": "Descargado con: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Elige idioma / Choose language / Выберите язык / اختر اللغة:",
        "language_changed": "✅ Idioma cambiado a español",
        "current_language": "🇪🇸 Español",
        
        # Админ команды
        "logs_enabled": "Registros habilitados ✅",
        "logs_disabled": "Registros deshabilitados 🚫",
        "cache_cleared": "🧹 ¡Caché limpiado!\nRegistros: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Creando transmisión</b>\n\n"
            "👥 Usuarios en base de datos: <b>{user_count}</b>\n\n"
            "Envía cualquier mensaje para transmisión:\n"
            "• 📝 Texto\n"
            "• 🖼️ Imagen\n"
            "• 📹 Video\n"
            "• 📄 Documento\n"
            "• 🎵 Audio"
        ),
        "broadcast_no_users": "❌ No hay usuarios para transmisión",
        "broadcast_confirm": (
            "📢 <b>Confirmación de transmisión</b>\n\n"
            "👥 Destinatarios: <b>{user_count}</b>\n"
            "📝 Tipo: {message_type}\n\n"
            "Haz clic en 'Enviar transmisión' para confirmar:"
        ),
        "broadcast_send": "✅ Enviar transmisión",
        "broadcast_cancel": "❌ Cancelar",
        "broadcast_preview": "👁️ Vista previa",
        "broadcast_stats": "📊 Estadísticas de usuarios",
        "broadcast_sending": "📤 Enviando transmisión...",
        "broadcast_completed": (
            "📢 <b>¡Transmisión completada!</b>\n\n"
            "✅ Enviado exitosamente: <b>{success_count}</b>\n"
            "❌ Errores: <b>{error_count}</b>\n"
            "👥 Total de destinatarios: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Transmisión cancelada.",
        "broadcast_reset": "✅ Estado de transmisión reiniciado",
        "broadcast_no_state": "ℹ️ No hay estado de transmisión activo",
        "broadcast_preview_text": "👁️ <b>Vista previa de transmisión:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Texto",
        "message_type_photo": "🖼️ Imagen",
        "message_type_video": "📹 Video",
        "message_type_document": "📄 Documento",
        "message_type_audio": "🎵 Audio",
    },
    
    "fr": {
        # Стартовое сообщение
        "start_private": (
            "👋 Salut ! Je t'aide à télécharger des vidéos TikTok sans filigrane ! 🚀\n\n"
            "📎 Envoie un lien de vidéo TikTok et je te renverrai le fichier sans filigrane ! ✨\n\n"
            "💡 Tu peux m'ajouter à un chat pour une utilisation pratique ! 😊\n\n"
            "🌐 Utilise /lang pour changer de langue"
        ),
        "start_group": (
            "🎉 Salut, {chat_title} ! 👋\n\n"
            "🤖 Je suis un bot pour télécharger des vidéos TikTok sans filigrane ! 🚀\n\n"
            "📎 Envoie simplement un lien de vidéo TikTok et je te renverrai le fichier sans filigrane ! ✨\n\n"
            "⚠️ J'ai besoin des droits d'administrateur pour travailler dans le chat ! 👑\n\n"
            "💡 Je travaille rapidement et efficacement ! 😊\n\n"
            "🌐 Utilise /lang pour changer de langue"
        ),
        "add_to_chat": "➕ Ajouter au chat",
        
        # Ошибки
        "invalid_link": (
            "❌ Lien TikTok invalide.\n\n"
            "Pour télécharger une vidéo, envoie un lien au format :\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Impossible d'obtenir la vidéo. Vérifie le lien ou réessaie plus tard.",
        "service_unavailable": "🔧 Service temporairement indisponible. Recherche d'un API stable...",
        "invalid_video_url": "❌ URL de vidéo invalide reçue. Essaie un autre lien.",
        
        # Прогресс
        "progress_start": "⏳ Démarrage du téléchargement...",
        "progress_analyzing": "🔍 Analyse du lien...",
        "progress_getting": "🎥 Obtention de la vidéo...",
        "progress_downloading": "📥 Téléchargement du fichier...",
        "progress_sending": "📤 Envoi de la vidéo...",
        
        # Подпись видео
        "video_caption": "Téléchargé avec : @{bot_username}",
        
        # Языки
        "language_select": "🌐 Choisis la langue / Choose language / Выберите язык / اختر اللغة / Elige idioma :",
        "language_changed": "✅ Langue changée en français",
        "current_language": "🇫🇷 Français",
        
        # Админ команды
        "logs_enabled": "Journaux activés ✅",
        "logs_disabled": "Journaux désactivés 🚫",
        "cache_cleared": "🧹 Cache vidé !\nEnregistrements : {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Création de diffusion</b>\n\n"
            "👥 Utilisateurs en base de données : <b>{user_count}</b>\n\n"
            "Envoie n'importe quel message pour diffusion :\n"
            "• 📝 Texte\n"
            "• 🖼️ Image\n"
            "• 📹 Vidéo\n"
            "• 📄 Document\n"
            "• 🎵 Audio"
        ),
        "broadcast_no_users": "❌ Aucun utilisateur pour diffusion",
        "broadcast_confirm": (
            "📢 <b>Confirmation de diffusion</b>\n\n"
            "👥 Destinataires : <b>{user_count}</b>\n"
            "📝 Type : {message_type}\n\n"
            "Clique sur 'Envoyer diffusion' pour confirmer :"
        ),
        "broadcast_send": "✅ Envoyer diffusion",
        "broadcast_cancel": "❌ Annuler",
        "broadcast_preview": "👁️ Aperçu",
        "broadcast_stats": "📊 Statistiques des utilisateurs",
        "broadcast_sending": "📤 Envoi de diffusion...",
        "broadcast_completed": (
            "📢 <b>Diffusion terminée !</b>\n\n"
            "✅ Envoyé avec succès : <b>{success_count}</b>\n"
            "❌ Erreurs : <b>{error_count}</b>\n"
            "👥 Total des destinataires : <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Diffusion annulée.",
        "broadcast_reset": "✅ État de diffusion réinitialisé",
        "broadcast_no_state": "ℹ️ Aucun état de diffusion actif",
        "broadcast_preview_text": "👁️ <b>Aperçu de diffusion :</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Texte",
        "message_type_photo": "🖼️ Image",
        "message_type_video": "📹 Vidéo",
        "message_type_document": "📄 Document",
        "message_type_audio": "🎵 Audio",
    },
    
    "de": {
        # Стартовое сообщение
        "start_private": (
            "👋 Hallo! Ich helfe dir dabei, TikTok-Videos ohne Wasserzeichen herunterzuladen! 🚀\n\n"
            "📎 Sende einen TikTok-Video-Link und ich sende dir die Datei ohne Wasserzeichen zurück! ✨\n\n"
            "💡 Du kannst mich zu einem Chat hinzufügen für bequeme Nutzung! 😊\n\n"
            "🌐 Verwende /lang um die Sprache zu ändern"
        ),
        "start_group": (
            "🎉 Hallo, {chat_title}! 👋\n\n"
            "🤖 Ich bin ein Bot zum Herunterladen von TikTok-Videos ohne Wasserzeichen! 🚀\n\n"
            "📎 Sende einfach einen TikTok-Video-Link und ich sende dir die Datei ohne Wasserzeichen zurück! ✨\n\n"
            "⚠️ Ich brauche Admin-Rechte um im Chat zu arbeiten! 👑\n\n"
            "💡 Ich arbeite schnell und effizient! 😊\n\n"
            "🌐 Verwende /lang um die Sprache zu ändern"
        ),
        "add_to_chat": "➕ Zum Chat hinzufügen",
        
        # Ошибки
        "invalid_link": (
            "❌ Ungültiger TikTok-Link.\n\n"
            "Um ein Video herunterzuladen, sende einen Link im Format:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Video konnte nicht abgerufen werden. Überprüfe den Link oder versuche es später erneut.",
        "service_unavailable": "🔧 Service vorübergehend nicht verfügbar. Suche nach einer stabilen API...",
        "invalid_video_url": "❌ Ungültige Video-URL erhalten. Versuche einen anderen Link.",
        
        # Прогресс
        "progress_start": "⏳ Download wird gestartet...",
        "progress_analyzing": "🔍 Link wird analysiert...",
        "progress_getting": "🎥 Video wird abgerufen...",
        "progress_downloading": "📥 Datei wird heruntergeladen...",
        "progress_sending": "📤 Video wird gesendet...",
        
        # Подпись видео
        "video_caption": "Heruntergeladen mit: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Wähle die Sprache / Choose language / Выберите язык / اختر اللغة / Elige idioma / Choisis la langue :",
        "language_changed": "✅ Sprache auf Deutsch geändert",
        "current_language": "🇩🇪 Deutsch",
        
        # Админ команды
        "logs_enabled": "Logs aktiviert ✅",
        "logs_disabled": "Logs deaktiviert 🚫",
        "cache_cleared": "🧹 Cache geleert!\nEinträge: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Broadcast erstellen</b>\n\n"
            "👥 Benutzer in der Datenbank: <b>{user_count}</b>\n\n"
            "Sende eine beliebige Nachricht für den Broadcast:\n"
            "• 📝 Text\n"
            "• 🖼️ Bild\n"
            "• 📹 Video\n"
            "• 📄 Dokument\n"
            "• 🎵 Audio"
        ),
        "broadcast_no_users": "❌ Keine Benutzer für Broadcast",
        "broadcast_confirm": (
            "📢 <b>Broadcast bestätigen</b>\n\n"
            "👥 Empfänger: <b>{user_count}</b>\n"
            "📝 Typ: {message_type}\n\n"
            "Klicke 'Broadcast senden' zum Bestätigen:"
        ),
        "broadcast_send": "✅ Broadcast senden",
        "broadcast_cancel": "❌ Abbrechen",
        "broadcast_preview": "👁️ Vorschau",
        "broadcast_stats": "📊 Benutzerstatistiken",
        "broadcast_sending": "📤 Broadcast wird gesendet...",
        "broadcast_completed": (
            "📢 <b>Broadcast abgeschlossen!</b>\n\n"
            "✅ Erfolgreich gesendet: <b>{success_count}</b>\n"
            "❌ Fehler: <b>{error_count}</b>\n"
            "👥 Gesamte Empfänger: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Broadcast abgebrochen.",
        "broadcast_reset": "✅ Broadcast-Status zurückgesetzt",
        "broadcast_no_state": "ℹ️ Kein aktiver Broadcast-Status",
        "broadcast_preview_text": "👁️ <b>Broadcast-Vorschau:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Text",
        "message_type_photo": "🖼️ Bild",
        "message_type_video": "📹 Video",
        "message_type_document": "📄 Dokument",
        "message_type_audio": "🎵 Audio",
    },
    
    "pt": {
        # Стартовое сообщение
        "start_private": (
            "👋 Olá! Vou te ajudar a baixar vídeos do TikTok sem marca d'água! 🚀\n\n"
            "📎 Envie um link de vídeo do TikTok e eu retornarei o arquivo sem marca d'água! ✨\n\n"
            "💡 Você pode me adicionar a um chat para uso conveniente! 😊\n\n"
            "🌐 Use /lang para alterar o idioma"
        ),
        "start_group": (
            "🎉 Olá, {chat_title}! 👋\n\n"
            "🤖 Sou um bot para baixar vídeos do TikTok sem marca d'água! 🚀\n\n"
            "📎 Apenas envie um link de vídeo do TikTok e eu retornarei o arquivo sem marca d'água! ✨\n\n"
            "⚠️ Preciso de direitos de administrador para trabalhar no chat! 👑\n\n"
            "💡 Trabalho rápido e eficientemente! 😊\n\n"
            "🌐 Use /lang para alterar o idioma"
        ),
        "add_to_chat": "➕ Adicionar ao chat",
        
        # Ошибки
        "invalid_link": (
            "❌ Link do TikTok inválido.\n\n"
            "Para baixar um vídeo, envie um link no formato:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Falha ao obter o vídeo. Verifique o link ou tente novamente mais tarde.",
        "service_unavailable": "🔧 Serviço temporariamente indisponível. Procurando por uma API estável...",
        "invalid_video_url": "❌ URL de vídeo inválida recebida. Tente outro link.",
        
        # Прогресс
        "progress_start": "⏳ Iniciando download...",
        "progress_analyzing": "🔍 Analisando link...",
        "progress_getting": "🎥 Obtendo vídeo...",
        "progress_downloading": "📥 Baixando arquivo...",
        "progress_sending": "📤 Enviando vídeo...",
        
        # Подпись видео
        "video_caption": "Baixado com: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Escolha o idioma / Choose language / Выберите язык / اختر اللغة / Elige idioma / Choisis la langue / Wähle die Sprache :",
        "language_changed": "✅ Idioma alterado para português",
        "current_language": "🇵🇹 Português",
        
        # Админ команды
        "logs_enabled": "Logs ativados ✅",
        "logs_disabled": "Logs desativados 🚫",
        "cache_cleared": "🧹 Cache limpo!\nEntradas: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Criando transmissão</b>\n\n"
            "👥 Usuários na base de dados: <b>{user_count}</b>\n\n"
            "Envie qualquer mensagem para transmissão:\n"
            "• 📝 Texto\n"
            "• 🖼️ Imagem\n"
            "• 📹 Vídeo\n"
            "• 📄 Documento\n"
            "• 🎵 Áudio"
        ),
        "broadcast_no_users": "❌ Nenhum usuário para transmissão",
        "broadcast_confirm": (
            "📢 <b>Confirmação de transmissão</b>\n\n"
            "👥 Destinatários: <b>{user_count}</b>\n"
            "📝 Tipo: {message_type}\n\n"
            "Clique em 'Enviar transmissão' para confirmar:"
        ),
        "broadcast_send": "✅ Enviar transmissão",
        "broadcast_cancel": "❌ Cancelar",
        "broadcast_preview": "👁️ Visualizar",
        "broadcast_stats": "📊 Estatísticas dos usuários",
        "broadcast_sending": "📤 Enviando transmissão...",
        "broadcast_completed": (
            "📢 <b>Transmissão concluída!</b>\n\n"
            "✅ Enviado com sucesso: <b>{success_count}</b>\n"
            "❌ Erros: <b>{error_count}</b>\n"
            "👥 Total de destinatários: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Transmissão cancelada.",
        "broadcast_reset": "✅ Estado da transmissão redefinido",
        "broadcast_no_state": "ℹ️ Nenhum estado de transmissão ativo",
        "broadcast_preview_text": "👁️ <b>Visualização da transmissão:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Texto",
        "message_type_photo": "🖼️ Imagem",
        "message_type_video": "📹 Vídeo",
        "message_type_document": "📄 Documento",
        "message_type_audio": "🎵 Áudio",
    },
    
    "ja": {
        # Стартовое сообщение
        "start_private": (
            "👋 こんにちは！TikTokの動画を透かしなしでダウンロードするお手伝いをします！🚀\n\n"
            "📎 TikTokの動画リンクを送信すると、透かしなしのファイルをお返しします！✨\n\n"
            "💡 便利な使用のためにチャットに追加できます！😊\n\n"
            "🌐 言語を変更するには /lang を使用してください"
        ),
        "start_group": (
            "🎉 こんにちは、{chat_title}！👋\n\n"
            "🤖 TikTokの動画を透かしなしでダウンロードするボットです！🚀\n\n"
            "📎 TikTokの動画リンクを送信するだけで、透かしなしのファイルをお返しします！✨\n\n"
            "⚠️ チャットで動作するには管理者権限が必要です！👑\n\n"
            "💡 高速で効率的に動作します！😊\n\n"
            "🌐 言語を変更するには /lang を使用してください"
        ),
        "add_to_chat": "➕ チャットに追加",
        
        # Ошибки
        "invalid_link": (
            "❌ 無効なTikTokリンクです。\n\n"
            "動画をダウンロードするには、以下の形式でリンクを送信してください：\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ 動画を取得できませんでした。リンクを確認するか、後でもう一度お試しください。",
        "service_unavailable": "🔧 サービスが一時的に利用できません。安定したAPIを検索中...",
        "invalid_video_url": "❌ 無効な動画URLが受信されました。別のリンクをお試しください。",
        
        # Прогресс
        "progress_start": "⏳ ダウンロードを開始しています...",
        "progress_analyzing": "🔍 リンクを分析しています...",
        "progress_getting": "🎥 動画を取得しています...",
        "progress_downloading": "📥 ファイルをダウンロードしています...",
        "progress_sending": "📤 動画を送信しています...",
        
        # Подпись видео
        "video_caption": "ダウンロード元：@{bot_username}",
        
        # Языки
        "language_select": "🌐 言語を選択 / Choose language / Выберите язык / اختر اللغة / Elige idioma / Choisis la langue / Wähle die Sprache / Escolha o idioma :",
        "language_changed": "✅ 言語が日本語に変更されました",
        "current_language": "🇯🇵 日本語",
        
        # Админ команды
        "logs_enabled": "ログが有効になりました ✅",
        "logs_disabled": "ログが無効になりました 🚫",
        "cache_cleared": "🧹 キャッシュがクリアされました！\nエントリ：{size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>ブロードキャストの作成</b>\n\n"
            "👥 データベース内のユーザー：<b>{user_count}</b>\n\n"
            "ブロードキャスト用に任意のメッセージを送信：\n"
            "• 📝 テキスト\n"
            "• 🖼️ 画像\n"
            "• 📹 動画\n"
            "• 📄 ドキュメント\n"
            "• 🎵 オーディオ"
        ),
        "broadcast_no_users": "❌ ブロードキャスト用のユーザーがありません",
        "broadcast_confirm": (
            "📢 <b>ブロードキャストの確認</b>\n\n"
            "👥 受信者：<b>{user_count}</b>\n"
            "📝 タイプ：{message_type}\n\n"
            "確認するには「ブロードキャストを送信」をクリック："
        ),
        "broadcast_send": "✅ ブロードキャストを送信",
        "broadcast_cancel": "❌ キャンセル",
        "broadcast_preview": "👁️ プレビュー",
        "broadcast_stats": "📊 ユーザー統計",
        "broadcast_sending": "📤 ブロードキャストを送信中...",
        "broadcast_completed": (
            "📢 <b>ブロードキャストが完了しました！</b>\n\n"
            "✅ 正常に送信：<b>{success_count}</b>\n"
            "❌ エラー：<b>{error_count}</b>\n"
            "👥 総受信者：<b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ ブロードキャストがキャンセルされました。",
        "broadcast_reset": "✅ ブロードキャスト状態がリセットされました",
        "broadcast_no_state": "ℹ️ アクティブなブロードキャスト状態がありません",
        "broadcast_preview_text": "👁️ <b>ブロードキャストプレビュー：</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 テキスト",
        "message_type_photo": "🖼️ 画像",
        "message_type_video": "📹 動画",
        "message_type_document": "📄 ドキュメント",
        "message_type_audio": "🎵 オーディオ",
    },
    
    "pl": {
        # Стартовое сообщение
        "start_private": (
            "👋 Cześć! Pomogę Ci pobrać filmy z TikTok bez znaku wodnego! 🚀\n\n"
            "📎 Wyślij link do filmu TikTok, a zwrócę plik bez znaku wodnego! ✨\n\n"
            "💡 Możesz dodać mnie do czatu dla wygodnego użytkowania! 😊\n\n"
            "🌐 Użyj /lang aby zmienić język"
        ),
        "start_group": (
            "🎉 Cześć, {chat_title}! 👋\n\n"
            "🤖 Jestem botem do pobierania filmów z TikTok bez znaku wodnego! 🚀\n\n"
            "📎 Po prostu wyślij link do filmu TikTok, a zwrócę plik bez znaku wodnego! ✨\n\n"
            "⚠️ Potrzebuję uprawnień administratora aby działać w czacie! 👑\n\n"
            "💡 Działam szybko i efektywnie! 😊\n\n"
            "🌐 Użyj /lang aby zmienić język"
        ),
        "add_to_chat": "➕ Dodaj do czatu",
        
        # Ошибки
        "invalid_link": (
            "❌ Nieprawidłowy link TikTok.\n\n"
            "Aby pobrać film, wyślij link w formacie:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Nie udało się pobrać filmu. Sprawdź link lub spróbuj ponownie później.",
        "service_unavailable": "🔧 Usługa tymczasowo niedostępna. Szukam stabilnego API...",
        "invalid_video_url": "❌ Otrzymano nieprawidłowy URL filmu. Spróbuj innego linku.",
        
        # Прогресс
        "progress_start": "⏳ Rozpoczynam pobieranie...",
        "progress_analyzing": "🔍 Analizuję link...",
        "progress_getting": "🎥 Pobieram film...",
        "progress_downloading": "📥 Pobieram plik...",
        "progress_sending": "📤 Wysyłam film...",
        
        # Подпись видео
        "video_caption": "Pobrano za pomocą: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Wybierz język / Choose language / Выберите язык / اختر اللغة / Elige idioma / Choisis la langue / Wähle die Sprache / Escolha o idioma / 言語を選択 :",
        "language_changed": "✅ Język zmieniony na polski",
        "current_language": "🇵🇱 Polski",
        
        # Админ команды
        "logs_enabled": "Logi włączone ✅",
        "logs_disabled": "Logi wyłączone 🚫",
        "cache_cleared": "🧹 Cache wyczyszczony!\nWpisy: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Tworzenie transmisji</b>\n\n"
            "👥 Użytkownicy w bazie danych: <b>{user_count}</b>\n\n"
            "Wyślij dowolną wiadomość do transmisji:\n"
            "• 📝 Tekst\n"
            "• 🖼️ Obraz\n"
            "• 📹 Film\n"
            "• 📄 Dokument\n"
            "• 🎵 Audio"
        ),
        "broadcast_no_users": "❌ Brak użytkowników do transmisji",
        "broadcast_confirm": (
            "📢 <b>Potwierdzenie transmisji</b>\n\n"
            "👥 Odbiorcy: <b>{user_count}</b>\n"
            "📝 Typ: {message_type}\n\n"
            "Kliknij 'Wyślij transmisję' aby potwierdzić:"
        ),
        "broadcast_send": "✅ Wyślij transmisję",
        "broadcast_cancel": "❌ Anuluj",
        "broadcast_preview": "👁️ Podgląd",
        "broadcast_stats": "📊 Statystyki użytkowników",
        "broadcast_sending": "📤 Wysyłanie transmisji...",
        "broadcast_completed": (
            "📢 <b>Transmisja zakończona!</b>\n\n"
            "✅ Pomyślnie wysłano: <b>{success_count}</b>\n"
            "❌ Błędy: <b>{error_count}</b>\n"
            "👥 Łącznie odbiorców: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Transmisja anulowana.",
        "broadcast_reset": "✅ Stan transmisji zresetowany",
        "broadcast_no_state": "ℹ️ Brak aktywnego stanu transmisji",
        "broadcast_preview_text": "👁️ <b>Podgląd transmisji:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Tekst",
        "message_type_photo": "🖼️ Obraz",
        "message_type_video": "📹 Film",
        "message_type_document": "📄 Dokument",
        "message_type_audio": "🎵 Audio",
    },
    
    "tr": {
        # Стартовое сообщение
        "start_private": (
            "👋 Merhaba! TikTok videolarını filigran olmadan indirmenize yardımcı olacağım! 🚀\n\n"
            "📎 TikTok video bağlantısı gönderin, filigran olmayan dosyayı size geri vereceğim! ✨\n\n"
            "💡 Kolay kullanım için beni bir sohbete ekleyebilirsiniz! 😊\n\n"
            "🌐 Dil değiştirmek için /lang kullanın"
        ),
        "start_group": (
            "🎉 Merhaba, {chat_title}! 👋\n\n"
            "🤖 TikTok videolarını filigran olmadan indiren bir botum! 🚀\n\n"
            "📎 Sadece TikTok video bağlantısı gönderin, filigran olmayan dosyayı size geri vereceğim! ✨\n\n"
            "⚠️ Sohbette çalışmak için yönetici yetkilerine ihtiyacım var! 👑\n\n"
            "💡 Hızlı ve verimli çalışırım! 😊\n\n"
            "🌐 Dil değiştirmek için /lang kullanın"
        ),
        "add_to_chat": "➕ Sohbete ekle",
        
        # Ошибки
        "invalid_link": (
            "❌ Geçersiz TikTok bağlantısı.\n\n"
            "Video indirmek için şu formatta bir bağlantı gönderin:\n"
            "https://vm.tiktok.com/XXXXXXX/"
        ),
        "download_error": "❌ Video alınamadı. Bağlantıyı kontrol edin veya daha sonra tekrar deneyin.",
        "service_unavailable": "🔧 Hizmet geçici olarak kullanılamıyor. Kararlı bir API arıyorum...",
        "invalid_video_url": "❌ Geçersiz video URL'si alındı. Başka bir bağlantı deneyin.",
        
        # Прогресс
        "progress_start": "⏳ İndirme başlatılıyor...",
        "progress_analyzing": "🔍 Bağlantı analiz ediliyor...",
        "progress_getting": "🎥 Video alınıyor...",
        "progress_downloading": "📥 Dosya indiriliyor...",
        "progress_sending": "📤 Video gönderiliyor...",
        
        # Подпись видео
        "video_caption": "İndirildi: @{bot_username}",
        
        # Языки
        "language_select": "🌐 Dil seçin / Choose language / Выберите язык / اختر اللغة / Elige idioma / Choisis la langue / Wähle die Sprache / Escolha o idioma / 言語を選択 / Wybierz język :",
        "language_changed": "✅ Dil Türkçe olarak değiştirildi",
        "current_language": "🇹🇷 Türkçe",
        
        # Админ команды
        "logs_enabled": "Loglar etkinleştirildi ✅",
        "logs_disabled": "Loglar devre dışı bırakıldı 🚫",
        "cache_cleared": "🧹 Önbellek temizlendi!\nGirişler: {size}/{max_size}",
        
        # Рассылка
        "broadcast_start": (
            "📢 <b>Yayın oluşturma</b>\n\n"
            "👥 Veritabanındaki kullanıcılar: <b>{user_count}</b>\n\n"
            "Yayın için herhangi bir mesaj gönderin:\n"
            "• 📝 Metin\n"
            "• 🖼️ Resim\n"
            "• 📹 Video\n"
            "• 📄 Belge\n"
            "• 🎵 Ses"
        ),
        "broadcast_no_users": "❌ Yayın için kullanıcı yok",
        "broadcast_confirm": (
            "📢 <b>Yayın onayı</b>\n\n"
            "👥 Alıcılar: <b>{user_count}</b>\n"
            "📝 Tür: {message_type}\n\n"
            "Onaylamak için 'Yayını gönder' tıklayın:"
        ),
        "broadcast_send": "✅ Yayını gönder",
        "broadcast_cancel": "❌ İptal",
        "broadcast_preview": "👁️ Önizleme",
        "broadcast_stats": "📊 Kullanıcı istatistikleri",
        "broadcast_sending": "📤 Yayın gönderiliyor...",
        "broadcast_completed": (
            "📢 <b>Yayın tamamlandı!</b>\n\n"
            "✅ Başarıyla gönderildi: <b>{success_count}</b>\n"
            "❌ Hatalar: <b>{error_count}</b>\n"
            "👥 Toplam alıcı: <b>{total_count}</b>"
        ),
        "broadcast_cancelled": "❌ Yayın iptal edildi.",
        "broadcast_reset": "✅ Yayın durumu sıfırlandı",
        "broadcast_no_state": "ℹ️ Aktif yayın durumu yok",
        "broadcast_preview_text": "👁️ <b>Yayın önizlemesi:</b>\n\n{content}",
        
        # Типы сообщений
        "message_type_text": "📝 Metin",
        "message_type_photo": "🖼️ Resim",
        "message_type_video": "📹 Video",
        "message_type_document": "📄 Belge",
        "message_type_audio": "🎵 Ses",
    }
}


class Localization:
    """Класс для работы с локализацией"""
    
    def __init__(self, language: Language = "ru") -> None:
        self._language = language
        self._logger = logging.getLogger(__name__)
    
    @property
    def language(self) -> Language:
        return self._language
    
    def get(self, key: str, **kwargs: Any) -> str:
        """Получить переведенный текст"""
        if self._language not in TRANSLATIONS:
            self._logger.warning("Language %s not found, using Russian", self._language)
            language = "ru"
        else:
            language = self._language
            
        if key not in TRANSLATIONS[language]:
            self._logger.warning("Translation key '%s' not found for language %s", key, language)
            return key
            
        text = TRANSLATIONS[language][key]
        
        # Заменяем параметры
        try:
            return text.format(**kwargs)
        except KeyError as e:
            self._logger.warning("Missing parameter %s for key '%s'", e, key)
            return text
    
    def get_language_keyboard(self) -> InlineKeyboardMarkup:
        """Получить клавиатуру для выбора языка"""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🇷🇺 Русский",
                        callback_data="lang:ru"
                    ),
                    InlineKeyboardButton(
                        text="🇺🇸 English", 
                        callback_data="lang:en"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇪🇸 Español",
                        callback_data="lang:es"
                    ),
                    InlineKeyboardButton(
                        text="🇫🇷 Français",
                        callback_data="lang:fr"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇩🇪 Deutsch",
                        callback_data="lang:de"
                    ),
                    InlineKeyboardButton(
                        text="🇵🇹 Português",
                        callback_data="lang:pt"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇯🇵 日本語",
                        callback_data="lang:ja"
                    ),
                    InlineKeyboardButton(
                        text="🇵🇱 Polski",
                        callback_data="lang:pl"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇹🇷 Türkçe",
                        callback_data="lang:tr"
                    ),
                    InlineKeyboardButton(
                        text="🇸🇦 العربية",
                        callback_data="lang:ar"
                    )
                ]
            ]
        )


# Глобальные экземпляры локализации
ru_loc = Localization("ru")
en_loc = Localization("en")


def get_localization(language: Language = "ru") -> Localization:
    """Получить экземпляр локализации для языка"""
    return Localization(language)
