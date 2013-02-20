<?php
require_once("classes/global.php");
class DataParser extends Core{
	public function __contructor(){
		parent::__constructor();
	}
	private function withQID($query, $id){
		$this->db->RunQuery(sprintf($this->db->qArr[$query],$id));
		$ret = array();
		while($row = $this->db->fetch()){
			$ret[] = $row;
		}
		return json_encode($ret);
	}
	public function itemsByTag($tag_id){
		return $this->withQID("selectItemsByTag",$tag_id);
	}
	public function tagsByItem($item_id){
		return $this->withQID("selectTagsByItem",$item_id);
	}
	public function randomTags(){
		return $this->withQID("selectRandomTags","");
	}
	public function allItems(){
		return $this->withQID("selectAllItems","");
	}
};
$puller = new DataParser();

//parse_str(implode('&', array_slice($argv, 1)), $_GET);

if(isset($_GET['get']))
	if ($_GET['get'] == "items"){
		if(isset($_GET['tag_id'])){
			$int = (int)($_GET['tag_id']);
			echo $puller->itemsByTag($int);
		} else {
			echo $puller->allItems();
		}
	} else if ($_GET['get'] == "tags"){
		if(isset($_GET['item_id'])){
			$int = (int)($_GET['item_id']);
			echo $puller->tagsByItem($int);
		} else {
			echo $puller->randomTags();		
		}	
	}
?>
