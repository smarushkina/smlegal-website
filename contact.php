<?php
// SM Legal — contact form handler (requires PHP mail() on the hosting server)
$to = 'office@smlegal.bg';
$lang = (isset($_POST['lang']) && $_POST['lang'] === 'en') ? 'en' : 'bg';
$back = $lang === 'en' ? '/en/contact.html' : '/kontakti.html';
function clean($v){ return trim(str_replace(["\r","\n"], ' ', strip_tags($v ?? ''))); }
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !empty($_POST['website'])) { header("Location: $back"); exit; }
$name = clean($_POST['name'] ?? ''); $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
$phone = clean($_POST['phone'] ?? ''); $company = clean($_POST['company'] ?? ''); $topic = clean($_POST['topic'] ?? '');
$message = trim(strip_tags($_POST['message'] ?? ''));
if (!$name || !$email || !$message || empty($_POST['consent'])) { header("Location: $back?error=1"); exit; }
$subject = '=?UTF-8?B?' . base64_encode('Запитване от smlegal.bg — ' . $name) . '?=';
$body = "Име: $name\nИмейл: $email\nТелефон: $phone\nКомпания: $company\nОбласт: $topic\nЕзик: $lang\n\n$message\n";
$headers = "From: SM Legal Website <no-reply@smlegal.bg>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$ok = @mail($to, $subject, $body, $headers);
header("Location: $back?" . ($ok ? 'sent=1' : 'error=1'));
