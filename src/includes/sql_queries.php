<?php
$sql_queries = array (
	"selectById" => "SELECT %s FROM `%s` WHERE id = %u",
	"deleteById" => "DROP FROM %s WHERE id = %u",
	"selectItemsByTag" => "SELECT I.id, I.name, I.location FROM relations R, items I WHERE I.id = R.itemID AND R.tagID = %d",
	"selectTagsByItem" => "SELECT T.id, T.tag FROM tags T, relations R WHERE R.itemID = %d AND T.id = R.tagID",
);
?>
