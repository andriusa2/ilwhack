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
	public function singleTag($id){
		return json_encode($this->qq->selectById('tag','tags',$id));
	}
	public function singleItem($id){
		return json_encode($this->qq->selectById('*','items',$id));
	}
	public function tagsByQuery($query){
		$res = array();
		foreach($query as $tag){
			if (strlen($tag) < 3) continue;
			$this->db->RunQuery(sprintf($this->db->qArr["selectTagsLikeQuery"],$tag));
			while ($row = $this->db->fetch()){
				$res [] = $row;
			}
		}
		return json_encode($res);
	}
};
$puller = new DataParser();

//parse_str(implode('&', array_slice($argv, 1)), $_GET);

if(isset($_GET['get']))
	if ($_GET['get'] == "items"){
		if(isset($_GET['tag_id'])){
			$int = (int)($_GET['tag_id']);
			echo $puller->itemsByTag($int);
		} else if(isset($_GET['id'])){
			$int = (int)($_GET['id']);
			echo $puller->singleItem($int);
		} else {
			echo $puller->allItems();
		}
	} else if ($_GET['get'] == "tags"){
		if(isset($_GET['item_id'])){
			$int = (int)($_GET['item_id']);
			echo $puller->tagsByItem($int);
		} else if(isset($_GET['id'])){
			$int = (int)($_GET['id']);
			echo $puller->singleTag($int);
		} else if(isset($_GET['query'])){
			$query = array();
			preg_match_all("/[a-z0-9]+/",strtolower($_GET['query']),$query);
			/* // php 5.3+
			$query = array_map(function($str){return trim($str);},$query);
			$query = array_map(function($str){return strtolower($str);},$query);
			*/
			echo $puller->tagsByQuery($query[0]);
		} else {
			echo $puller->randomTags();		
		}	
	}
?>
