from heapq import *

def bfs(costs, netlist, via, bend):
	ans = []
	for net in netlist:
		ans.append([])
		q = []
		found_route = False
		visited = [[[-1 for i in costs[0][0]] for j in costs[0]] for k in costs]
		pred = [[[[] for i in costs[0][0]] for j in costs[0]] for k in costs]
		heappush(q, (costs[net[1]][net[2]][net[3]], net[1:4]))
		costs[net[1]][net[2]][net[3]] = -1
		while q:
			(val, pos) = heappop(q)
			visited[pos[0]][pos[1]][pos[2]] = 1
			if(pos == net[4:]):
				found_route = True
				break
			for i in range(5):
				if(i==0):
					if((visited[1-pos[0]][pos[1]][pos[2]]==-1) and (costs[1-pos[0]][pos[1]][pos[2]]>-1)):
						pred[1-pos[0]][pos[1]][pos[2]] = pos
						visited[1-pos[0]][pos[1]][pos[2]] = 1
						heappush(q, (val+via+costs[1-pos[0]][pos[1]][pos[2]], [1-pos[0], pos[1], pos[2]]))
				else:
					next_pos = [pos[0], pos[1]+((i-1)//2)*(2*i-7), pos[2]+((4-i)//2)*(2*i-3)]
					if((next_pos[1]<0) or (next_pos[2]<0) or (next_pos[1]>=len(costs[0])) or (next_pos[2]>=len(costs[0][0]))):
						continue
					if(pos == net[1:4]):
						b=0
					else:
						b = int((next_pos[0] == pred[pos[0]][pos[1]][pos[2]][0]) and ((next_pos[1] == pred[pos[0]][pos[1]][pos[2]][1]) or (next_pos[2] == pred[pos[0]][pos[1]][pos[2]][2])))
					if((visited[next_pos[0]][next_pos[1]][next_pos[2]]==-1) and (costs[next_pos[0]][next_pos[1]][next_pos[2]])>-1):
						pred[next_pos[0]][next_pos[1]][next_pos[2]] = pos
						visited[next_pos[0]][next_pos[1]][next_pos[2]] = 1
						heappush(q, (val+b*bend+costs[next_pos[0]][next_pos[1]][next_pos[2]], next_pos))
		if found_route:
			while(pos !=  net[1:4]):
				costs[pos[0]][pos[1]][pos[2]] = -1
				ans[-1].append(pos)
				pos = pred[pos[0]][pos[1]][pos[2]]
			ans[-1].append(net[1:4])
	return ans

def route():
	file_list = ['bench1','bench2','bench3','bench4','bench5','industry1','fract2']
	for file in file_list:
		with open(str(file)+'.grid','r') as f:
			(x,y,bend,via) = map(int,f.readline().split())
			costs = [[[0 for i in range(y)] for j in range(x)] for k in range(2)]
			for i in range(2):
				for j in range(y):
					temp = list(map(int,f.readline().split()))
					for k in range(x):
						costs[i][k][j] = temp[k]
		with open(str(file)+'.nl','r') as f:
			n = int(f.readline())
			netlist = []
			for i in range(n):
				netlist.append(list(map(int,f.readline().split())))
				netlist[-1][1] -= 1
				netlist[-1][4] -= 1
		ans = bfs(costs, netlist, via, bend)
		print(file + ' COMPLETE')
		with open(str(file)+'.solution','a') as f:
			f.write(str(n)+'\n')
			for i in range(n):
				f.write(str(i+1)+'\n')
				ans[i].reverse()
				for j in range(len(ans[i])):
					ans[i][j][0] += 1
					for k in ans[i][j]:
						f.write(str(k))
					f.write('\n')
				f.write('0\n')
	return

route()