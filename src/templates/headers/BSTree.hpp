#ifndef BSTREE
#define BSTREE

#include <iostream>

template <class T> // árvore é do tipo nodeBlock
class BinaryTree
{

	struct node {
		T value;

		// struct nodeBlock {
		//     {% indexer_c_type %} userField;
		//     unsigned long long offset;
		// };

		struct node* right;
		struct node* left;
	};

public:
	BinaryTree();
	~BinaryTree();
	void add(T val);
	int size();
	bool lookup(T &nodeBlock); // lookup precisa de um nodeBlock

private:
	struct node* root;
	int treeSize;
	void add(struct node** node, T nodeBlock);
	bool lookup(struct node* node, T &nodeBlock);
	void deleteTree(struct node* node);
};

template <class T>
BinaryTree<T>::BinaryTree(){
	this->root = NULL;
	this->treeSize = 0;
}

template <class T>
BinaryTree<T>::~BinaryTree(){
	deleteTree(this->root);
}

template <class T>
int BinaryTree<T>::size(){
	return this->treeSize;
}

template <class T>
void BinaryTree<T>::add(T nodeBlock){
	add(&(this->root), nodeBlock);
}

template <class T>
void BinaryTree<T>::add(struct node** node, T nodeBlock){

	if (*node == NULL)	{
		struct node* tmp = new struct node;
		tmp->value = nodeBlock;
		tmp->left = NULL;
		tmp->right = NULL;
		*node = tmp;

		this->treeSize++;
	} else {
		if (nodeBlock.userField > (*node)->value.userField) {
			add(&(*node)->right, nodeBlock);
		} else {
			add(&(*node)->left, nodeBlock);
		}
	}
}

template <class T>
void BinaryTree<T>::deleteTree(struct node* node){
	if(node != NULL){
		deleteTree(node->left);
		deleteTree(node->right);
		delete node;
	}
}

template <class T>
bool BinaryTree<T>::lookup(T &nodeBlock){
	return lookup(this->root, nodeBlock);
}

template <class T>
bool BinaryTree<T>::lookup(struct node* node, T &nodeBlock){
	if (node == NULL) {
		return false;
	} else {
		if (nodeBlock.userField == node->value.userField) {
			nodeBlock.offset = node->value.offset;
			return true;
		}

		if (nodeBlock.userField > node->value.userField) {
			return lookup(node->right, nodeBlock);
		} else {
			return lookup(node->left, nodeBlock);
		}
	}
}

#endif // BSTREE
