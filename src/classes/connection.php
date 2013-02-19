<?php
require_once("includes/sql_queries.php");
class Database{
	/* database that we are working on */
	private $db = NULL;
	private $query = NULL;
	protected $result = NULL;
	public $qArr = NULL;
	public function __construct(){
		global $sql_queries;
		$this->qArr = &$sql_queries;
		$this->db = new mysqli(DB_HOST,DB_USERNAME,DB_PASSWORD,DB_NAME);
		$this->db->set_charset("utf8");
		if($this->db->connect_errno) $this->Error(CONNECT_ERROR);
	}
	private function Error($id){
		die("<h1>Database error:</h1><h2>{$this->db->error}</h2>");
	}
	public function runQuery($query){
		$this->result = $this -> db -> query($query);
		if (!$this->result) $this->Error(QUERY_ERROR);
	}
	public function fetch(){
		return $this->result->fetch_array();
	}
	public function clean(){
		return $this->db->real_escape_string($str);
	}
	public function numRows(){
		if ($this->result)
			return $this->result->num_rows();
		else
			return false;
	}
};
class QuickQuery{
	private $prep_queries = array();
	public function __construct($db){
		global $sql_queries;
		$this->prep_queries = &$sql_queries;
		$this->db = &$db;
	}
	public function SelectById($cols,$table,$id){
		$this->db->runQuery(sprintf($this->prep_queries["getById"],$cols, $table,$id));
		return $this->db->fetch();
	}
	public function DropById($cols, $table, $id){
		$this->db->runQuery(sprintf($this->prep_queries["dropById"], $table, $id));
		return true;
	}
};
?>
