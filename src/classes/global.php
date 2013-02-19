<?php
require_once("includes/define.php");
require_once("classes/connection.php");
class Core {
	public $qq = null;
	public $db = null;
	public function __construct(){
		$this->db = new Database();
		$this->qq = new QuickQuery($this->db);
	}	
};
?>
