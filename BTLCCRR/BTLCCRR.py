import networkx as nx
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    ma_tran_goc, do_thi_co_huong = nhap_du_lieu_tu_ban_phim()

    danh_sach_ke = ma_tran_sang_danh_sach_ke(ma_tran_goc)
    print("\n KẾT QUẢ CHUYỂN ĐỔI ")
    print(f"Danh sách kề: {danh_sach_ke}")

    danh_sach_canh = danh_sach_ke_sang_danh_sach_canh(danh_sach_ke, co_huong=do_thi_co_huong)
    print(f"Danh sách cạnh: {danh_sach_canh}")

    ve_va_luu_do_thi(danh_sach_canh, co_huong=do_thi_co_huong, ten_file="do_thi_nhap_tay.png")