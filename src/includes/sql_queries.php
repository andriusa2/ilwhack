<?php
$sql_queries = array (
	"selectById" => "SELECT %s FROM `%s` WHERE id = %d",
	"deleteById" => "DROP FROM %s WHERE id = %d",
	"selectItemsByTag" => "SELECT I.id, I.name, I.location FROM relations R, items I WHERE I.id = R.itemID AND R.tagID = %d",
	"selectTagsByItem" => "SELECT T.id, T.tag FROM tags T, relations R WHERE R.itemID = %d AND T.id = R.tagID",
	"selectRandomTags" => "SELECT * FROM tags ORDER BY RAND() LIMIT 20",
	"selectAllItems" => "SELECT * FROM items LIMIT 500"
);
?>
