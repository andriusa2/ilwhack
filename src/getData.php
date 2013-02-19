<?php
require_once("classes/global.php");
class DataParser extends Core{
	public function __contructor(){
		parent::__constructor();
	}
	public function itemsByTags($tag_id){
		$this->db->RunQuery(sprintf($this->db->qArr["selectItemsByTag"],$tag_id));
		$ret = array();
		while($row = $this->db->fetch()){
			$ret[] = $row;
		}
		return json_encode($ret);
	}
};
$puller = new DataParser();

parse_str(implode('&', array_slice($argv, 1)), $_GET);

if(isset($_GET['get']))
	if ($_GET['get'] == "items"){
		if(isset($_GET['tag_id'])){
			$int = (int)($_GET['tag_id']);
			echo $puller->itemsByTags($_GET['tag_id']);
		}
	}
?>
