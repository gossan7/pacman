Notes de ce qu'il faudra ajouter:

- il faut faire cette commande pour accorder les droits à pynput :

			xhost +SI:localuser:$(whoami)

- le sujet demandait que les ghosts chassent le pacman avec une ia qui leur et propre mais de fuir s'ils sont mangeables, du coup :
		- ia de chasse qui est celle des ghosts du jeu de base (pathfinding + prio des directions si égalité + ce qu'ils vont focus)
		- ia de fuite = inverse de l'ia de chasse
		- pas de mode scatter car va à l'encontre de la consigne