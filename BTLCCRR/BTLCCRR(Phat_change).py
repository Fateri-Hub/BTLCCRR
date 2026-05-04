import networkx as nx
import matplotlib.pyplot as plt
from collections import deque# để dùng popelft

def ma_tran_sang_danh_sach_ke(ma_tran):
    """Chuyển Ma trận kề -> Danh sách kề"""
    danh_sach_ke = {}
    so_dinh = len(ma_tran)
    for i in range(so_dinh):
        danh_sach_ke[i] = []
        for j in range(len(ma_tran[i])):
            if ma_tran[i][j] != 0:
                danh_sach_ke[i].append(j)
    return danh_sach_ke

def danh_sach_ke_sang_danh_sach_canh(danh_sach_ke, co_huong=False):
    """Chuyển Danh sách kề -> Danh sách cạnh"""
    danh_sach_canh = []
    for u in danh_sach_ke:
        for v in danh_sach_ke[u]:
            if not co_huong:
                if (v, u) not in danh_sach_canh:
                    danh_sach_canh.append((u, v))
            else:
                danh_sach_canh.append((u, v))
    return danh_sach_canh

def ve_va_luu_do_thi(danh_sach_canh, co_huong=False, ten_file="do_thi_cua_toi.png"):
    """Vẽ đồ thị trực quan và lưu thành file ảnh"""
    do_thi = nx.DiGraph() if co_huong else nx.Graph()
    do_thi.add_edges_from(danh_sach_canh)

    plt.figure(figsize=(7, 7))
    vi_tri_dinh = nx.spring_layout(do_thi, seed=42) 
    
    nx.draw(do_thi, vi_tri_dinh, 
            with_labels=True, 
            node_color='#ff9999', 
            node_size=2000, 
            edge_color='#666666', 
            font_size=16, 
            font_weight='bold',
            arrows=co_huong, 
            arrowsize=20,
            width=2)

    plt.savefig(ten_file, format="PNG", dpi=300) 
    print(f"\n Đã vẽ và lưu đồ thị thành công vào file: {ten_file}")
    plt.show()

def nhap_du_lieu_tu_ban_phim():
    """Nhập ma trận kề và cấu hình đồ thị từ người dùng"""
    print(" CHƯƠNG TRÌNH XỬ LÝ ĐỒ THỊ ")
    
    loai = input("Đồ thị có hướng không? (Nhập 'c' cho Có, 'k' cho Không): ").strip().lower()
    co_huong = True if loai == 'c' else False
    so_dinh = int(input("Nhập số lượng đỉnh: "))
    
    ma_tran_goc = []
    print(f"\nNhập ma trận kề ({so_dinh}x{so_dinh}):")
    
    for i in range(so_dinh):
        while True:
            try:
                dong_du_lieu = input(f"  - Dòng {i}: ").strip().split()
                dong = [int(x) for x in dong_du_lieu]
                
                if len(dong) != so_dinh:
                    print(f"    [Lỗi] Vui lòng nhập đúng {so_dinh} số.")
                    continue
                
                ma_tran_goc.append(dong)
                break
            except ValueError:
                print("    [Lỗi] Vui lòng chỉ nhập số nguyên.")
                
    return ma_tran_goc, co_huong


#Tim duong di ngan nhat(PHAT)
def shortest_path_bfs(danh_sach_ke, start, end):
    hang_doi = deque([[start]])
    da_tham = set()
    

    while hang_doi:
        path = hang_doi.popleft()
        last_node = path[-1]
        
        if last_node == end:
            return path


        if last_node not in da_tham:
            da_tham.add(last_node)
            
            for x in danh_sach_ke[last_node]:
                new_path = list(path)#sao chep duong cu
                new_path.append(x)
                hang_doi.append(new_path)#cập nhật điểm bắt đầu và điểm kết thúc
    return None



#Duyệt đồ thị theo các chiến lược: BFS & DFS & BIPARTITE(HAI)
def bfs(danh_sach_ke, start):
    da_tham = set()
    hang_doi = deque([start])
    ket_qua = []

    while hang_doi:
        u = hang_doi.popleft()
        if u not in da_tham:
            da_tham.add(u)
            ket_qua.append(u)

            for v in danh_sach_ke[u]:
                if v not in da_tham:
                    hang_doi.append(v)

    return ket_qua

def dfs(danh_sach_ke, u, da_tham=None, ket_qua=None):
    if da_tham is None:
        da_tham = set()
        ket_qua = []

    da_tham.add(u)
    ket_qua.append(u)

    for v in danh_sach_ke[u]:
        if v not in da_tham:
            dfs(danh_sach_ke, v, da_tham, ket_qua)

    return ket_qua

# ===== BIPARTITE =====
def kiem_tra_bipartite(danh_sach_ke):
    mau = {}  # lưu màu của mỗi đỉnh (0 hoặc 1)

    for dinh in danh_sach_ke:
        if dinh not in mau:
            hang_doi = deque([dinh])
            mau[dinh] = 0  # tô màu đầu tiên

            while hang_doi:
                u = hang_doi.popleft()

                for v in danh_sach_ke[u]:
                    if u == v:
                        return False

                    if v not in mau:
                        mau[v] = 1 - mau[u] 
                        hang_doi.append(v)
                    elif mau[v] == mau[u]:
                        return False  

    return True



#7.1 Prim
def prim_operation(ma_tran, start):
    so_dinh = len(ma_tran)
    so_canh = 0 
#đếm nodes
    for i in range(so_dinh):
        for j in range(so_dinh):# 2 for ==> combo 1-2 1-3 1-4 /...../
            if ma_tran[i][j] != 0:
                so_canh += 1
    path_prim = []

    da_chon = [False] * so_dinh #? cho all sai (~~ vô cực)
    da_chon[start] = True 

    so_canh = 0

    while so_canh < so_dinh -1:
        trongsoMIN = float('inf')#collocation cho trongsomin là lớn nhất
        u = v = -1

        for i in range(so_dinh):
            if da_chon[i]:
                for j in range(so_dinh):
                    if not da_chon[j] and ma_tran[i][j] != 0:#cos trongj soso
                        if ma_tran[i][j] < trongsoMIN:#>?
                            trongsoMIN = ma_tran[i][j]
                            u = i
                            v = j
        #them canh da chon
        path_prim.append((u, v, trongsoMIN))
        da_chon[v] = True
        so_canh += 1

    return path_prim  




#7.2 Kruskal
def kruskal_operation(ma_tran):#bản chất không cần start, còn lại same(chỉ cần so sánh trọng số)
    edges = []
    so_dinh = len(ma_tran)
    for i in range(so_dinh):
        for j in range(so_dinh):# 2 for ==> combo 1-2 1-3 1-4 /...../
            if ma_tran[i][j] != 0:
                edges.append((i, j, ma_tran[i][j]))


    for i in range(len(edges)): #ex edges = [1, 2, 5] [0, 1, 3]
        for j in range(i + 1, len(edges)):
            if edges[i][2] > edges[j][2]: 
                edges[i], edges[j] = edges[j], edges[i]
 #biến_mình_đặt[x][y] . x ở đây là index(vị trị) của cái tủ trong 1 CĂN PHÒNG LỚN, y ở đây là từ cái tủ đó lấy ra món đồ được đánh dấu trong cái tủ đó
    return edges






def nhap_tu_ban_phim_PRIM():
    print("NHẬP MA TRẬN TRỌNG SỐ (0 nếu không có cạnh)")

    so_dinh = int(input("nhập số đỉnh:"))
    ma_tran = []

    for i in range(so_dinh):
        while True:
            try:
                dong_du_lieu = input(f"  - Dòng {i}: ").strip().split()
                dong = [int(x) for x in dong_du_lieu]

                if len(dong) != so_dinh:
                    print(f"    [Lỗi] Vui lòng nhập đúng {so_dinh} số.")
                    continue

                # 
                if dong[i] != 0:
                    print("[Lỗi] Phần tử đường chéo phải = 0")
                    continue

                ma_tran.append(dong)
                break

            except ValueError:
                print("    [Lỗi] Vui lòng chỉ nhập số nguyên.")

    return ma_tran
        

    



if __name__ == "__main__":
    ma_tran_goc, do_thi_co_huong = nhap_du_lieu_tu_ban_phim()

    danh_sach_ke = ma_tran_sang_danh_sach_ke(ma_tran_goc)
    print("\n KẾT QUẢ CHUYỂN ĐỔI ")
    print(f"Danh sách kề: {danh_sach_ke}")

    danh_sach_canh = danh_sach_ke_sang_danh_sach_canh(danh_sach_ke, co_huong=do_thi_co_huong)
    print(f"Danh sách cạnh: {danh_sach_canh}")

    ve_va_luu_do_thi(danh_sach_canh, co_huong=do_thi_co_huong, ten_file="do_thi_nhap_tay.png")

    print("Dữ liệu:", danh_sach_ke)

    print("\n--- SHORTEST PATH (BFS) ---")#(PHAT)
    start = int(input("nhap dinh bat dau:"))
    end = int(input("nhap dinh ket thuc:"))
    path = shortest_path_bfs(danh_sach_ke, start, end)
    print("đường đi ngắn nhất:", path)

     
    print("BFS - DFS - BIPARTITE OPERATION")
    start = int(input("nhap dinh bat dau:"))

    print("\n--- BFS ---")
    print("BFS:", bfs(danh_sach_ke, start))

    print("\n--- DFS ---")
    print("DFS:", dfs(danh_sach_ke, start))

    print("\n--- BIPARTITE ---")
    if kiem_tra_bipartite(danh_sach_ke):
        print("→ Đồ thị là BIPARTITE")
    else:
        print("→ Đồ thị KHÔNG phải BIPARTITE")

    print("======TEST PRIM=======")
    ma_tran = nhap_tu_ban_phim_PRIM()
    start_prim = int(input("nhập điểm bắt đầu(prim):"))
    path_prim = prim_operation(ma_tran, start_prim)

    print("=====TEST_PRIM=====")
    print("ket qua:", path_prim)

    print("\nCÁC CẠNH TRONG MST:")
    for u, v, w in path_prim:
        print(f"{chr(u+65)} - {chr(v+65)} = {w}")#trọng số vẫn vậy nên khogno cần 
    

    print("=====TEST_Kruksal=====")
    ma_tran_kruksal = ma_tran
    ketqua_krsal = kruskal_operation(ma_tran_kruksal)
    print("ket qua:", ketqua_krsal)
   






