<?php
require_once("define.php");
require_once("connection.php");
class Core {
	public $qq;
	public $db;
	public function __construct(){
		$this->db = new Database();
		$this->qq = new QuickQuery($db);
	}
};
?>
