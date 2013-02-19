<?php
class Database{
	/* database that we are working on */
	private $db = NULL;
	private $query = NULL;
	protected $result = NULL;
	public function __construct(){
		$this->db = new mysqli(DB_HOST,DB_USERNAME,DB_PASSWORD,DB_NAME);
		$this->set_charset("utf8");
		if($this->db->connect_errno) $this->Error(CONNECT_ERROR);
	}
	private function Error($id){
		die("<h1>Database error:</h1><h2>{$this->db->error}</h2>");
	}
	public function RunQuery($query){
		$this->result = $this -> db -> query($this->query);
		if (!$this->result) $this->Error(QUERY_ERROR);
	}
	public function Fetch(){
		if($this->result) return $this->result->fetch_array();
		else $this->Error(RUNQUERY_ERROR);
	}
	public function clean(){
		return $this->db->real_escape_string($str);
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
		$this->db->RunQuery(sprintf($this->prep_queries["getById"],$cols, $table,$id));
		return $this->db->Fetch();
	}
	public function DropById($cols, $table, $id){
		$this->db->RunQuery(sprintf($this->prep_queries["dropById"], $table, $id));
		return true;
	}
};
?>
