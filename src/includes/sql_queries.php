<?php
$sql_queries = array (
	"getSiteSettings" => "SELECT * FROM `site_settings` WHERE id = 1 LIMIT 1",
	"getLatestNews" => "SELECT * FROM `news` ORDER BY datetime DESC LIMIT %u ,%u",
	"selectById" => "SELECT %s FROM `%s` WHERE id = %u",
	"deleteById" => "DROP FROM %s WHERE id = %u",
	"insert" => "INSERT INTO `%s` (%s) VALUES (%s)",
);
?>