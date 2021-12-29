import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

gates_map = {}

def opp_pads(x1,y1,x2,y2,pads,pads_x,pads_y):
	for i in range(len(pads)):
		if pads_x[i]<x1:
			pads_x[i] = x1
		elif pads_x[i]>x2:
			pads_x[i] = x2
		if pads_y[i]<y1:
			pads_y[i] = y1
		elif pads_y[i]>y2:
			pads_y[i] = y2
	return (pads, pads_x, pads_y)

def place(n_gates, n_pads, params, hor_vert=False, split_count=9):
	if(split_count==0):
		return
	x1 = params['x1']
	y1 = params['y1']
	x2 = params['x2']
	y2 = params['y2']
	gates = params['gates']
	gates_x = params['gates_x']
	gates_y = params['gates_y']
	pads = params['pads']
	pads_x = params['pads_x']
	pads_y = params['pads_y']
	C = params['C']
	C_mat = np.zeros((n_gates, n_gates))
	a_mat = np.zeros((n_gates, n_gates))
	b_x = np.zeros((n_gates,1))
	b_y = np.zeros((n_gates,1))
	for i in range(n_gates):
		for j in range(n_gates):
			C_mat[i][j] = C[gates[i]][gates[j]]
			a_mat[i][j] = -C_mat[i][j]
	for i in range(n_gates):
		a_mat[i][i] += np.sum(C_mat[i])
		for j in range(len(pads)):
			if(C[gates[i]][pads[j]]!=0):
				a_mat[i][i] += C[gates[i]][pads[j]]
				b_x[i][0] += pads_x[j]
				b_y[i][0] += pads_y[j]
	x = spsolve(csc_matrix(a_mat), csc_matrix(b_x))
	y = spsolve(csc_matrix(a_mat), csc_matrix(b_y))
	for i in range(n_gates):
		gates_map[gates[i]] = (x[i], y[i])
	gates_1 = []
	gates_2 = []
	gates_x_1 = []
	gates_y_1 = []
	gates_x_2 = []
	gates_y_2 = []

	pads_1 = pads.copy()
	pads_2 = pads.copy()
	pads_x_1 = pads_x.copy()
	pads_y_1 = pads_y.copy()
	pads_x_2 = pads_x.copy()
	pads_y_2 = pads_y.copy()

	if hor_vert:
		y_part = (y1+y2)/2
		y_mid = np.median(y)
		for i in range(n_gates):
			if y[i]>y_mid:
				gates_1.append(gates[i])
				gates_x_1.append(x[i])
				gates_y_1.append(y[i])
				pads_2.append(gates[i])
				pads_x_2.append(x[i])
				pads_y_2.append(y[i])
			else:
				gates_2.append(gates[i])
				gates_x_2.append(x[i])
				gates_y_2.append(y[i])
				pads_1.append(gates[i])
				pads_x_1.append(x[i])
				pads_y_1.append(y[i])
		(pads_1, pads_x_1, pads_y_1) = opp_pads(x1, y1, x2, y_part, pads_1, pads_x_1, pads_y_1)
		(pads_2, pads_x_2, pads_y_2) = opp_pads(x1, y_part, x2, y2, pads_2, pads_x_2, pads_y_2)
		place(len(gates_1), len(pads_2), {'x1':x1, 'y1':y_part, 'x2':x2, 'y2':y2, 'gates':gates_1, 'gates_x':gates_x_1, 'gates_y':gates_y_1, 'pads':pads_2, 'pads_x':pads_x_2, 'pads_y':pads_y_2, 'C':C}, not hor_vert, split_count-1)
		place(len(gates_2), len(pads_1), {'x1':x1, 'y1':y1, 'x2':x2, 'y2':y_part, 'gates':gates_2, 'gates_x':gates_x_2, 'gates_y':gates_y_2, 'pads':pads_1, 'pads_x':pads_x_1, 'pads_y':pads_y_1, 'C':C}, not hor_vert, split_count-1)
		return
	else:
		x_part = (x1+x2)/2
		x_mid = np.median(x)
		for i in range(n_gates):
			if x[i]>x_mid:
				gates_1.append(gates[i])
				gates_x_1.append(x[i])
				gates_y_1.append(y[i])
				pads_2.append(gates[i])
				pads_x_2.append(x[i])
				pads_y_2.append(y[i])
			else:
				gates_2.append(gates[i])
				gates_x_2.append(x[i])
				gates_y_2.append(y[i])
				pads_1.append(gates[i])
				pads_x_1.append(x[i])
				pads_y_1.append(y[i])
		(pads_1, pads_x_1, pads_y_1) = opp_pads(x1, y1, x_part, y2, pads_1, pads_x_1, pads_y_1)
		(pads_2, pads_x_2, pads_y_2) = opp_pads(x_part, y1, x2, y2, pads_2, pads_x_2, pads_y_2)
		place(len(gates_1), len(pads_2), {'x1':x_part, 'y1':y1, 'x2':x2, 'y2':y2, 'gates':gates_1, 'gates_x':gates_x_1, 'gates_y':gates_y_1, 'pads':pads_2, 'pads_x':pads_x_2, 'pads_y':pads_y_2, 'C':C}, not hor_vert, split_count-1)
		place(len(gates_2), len(pads_1), {'x1':x1, 'y1':y1, 'x2':x_part, 'y2':y2, 'gates':gates_2, 'gates_x':gates_x_2, 'gates_y':gates_y_2, 'pads':pads_1, 'pads_x':pads_x_1, 'pads_y':pads_y_1, 'C':C}, not hor_vert, split_count-1)
		return
	return

def main():
	file_arr = ['industry1','industry2','biomed']
	output_arr = ['industry1.txt','industry2.txt','biomed.txt']
	strings = ['industry1','industry2','biomed']
	for file in range(3):
		print('Placing of '+strings[file]+' started. Please wait some time.')
		with open(file_arr[file],'r') as f:
			(n_gates, n_nets) = map(int, f.readline().split())
			arr = [[] for i in range(n_nets)]
			gates = list(range(n_gates))
			gates_x = [0 for i in gates]
			gates_y = [0 for i in gates]

			for i in gates:
				gates_map[i] = (0,0)
				temp = list(map(int,f.readline().split()))
				for j in temp[2:]:
					arr[j-1].append(i)
			n_pads = int(f.readline())

			pads = list(range(n_gates, n_pads+n_gates))
			pads_x = []
			pads_y = []

			for i in pads:
				(_,net,x,y) = map(int, f.readline().split())
				arr[net-1].append(i)
				pads_x.append(x)
				pads_y.append(y)

			C = np.zeros((n_gates+n_pads, n_gates+n_pads))

			for i in range(n_nets):
				for j in arr[i]:
					for k in arr[i]:
						if j!=k:
							C[j][k] = 1
			place(n_gates, n_pads, {'x1':0, 'y1':0, 'x2':100, 'y2':100, 'gates':gates, 'gates_x':gates_x, 'gates_y':gates_y, 'pads':pads, 'pads_x':pads_x, 'pads_y':pads_y, 'C':C})

		print('Placement complete. Please check '+output_arr[file]+' for results')
		with open(output_arr[file],'a') as f:
			for i in range(n_gates):
				f.write(str(i+1) + ' ' + str(gates_map[i][0]) + ' ' + str(gates_map[i][1]) + '\n')
	return

main()