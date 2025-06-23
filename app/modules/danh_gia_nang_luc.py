class DanhGiaNangLuc:
    def __init__(self):
        self.nang_luc = {
            "toan": {"cap_do_1": 0, "cap_do_2": 0, "cap_do_3": 0},
            "tieng_viet": {"cap_do_1": 0, "cap_do_2": 0, "cap_do_3": 0}
        }

    def cap_nhat_diem(self, mon, cap_do, diem):
        if mon in self.nang_luc and cap_do in self.nang_luc[mon]:
            self.nang_luc[mon][cap_do] = max(self.nang_luc[mon][cap_do], diem)

    def lay_diem_cao_nhat(self, mon, cap_do):
        return self.nang_luc.get(mon, {}).get(cap_do, 0)

    def xep_loai_nang_luc(self, mon):
        diem_tb = 0
        count = 0
        if mon in self.nang_luc:
            for cap_do, diem in self.nang_luc[mon].items():
                diem_tb += diem
                count += 1
            diem_tb /= count if count else 1

            if diem_tb >= 8:
                return "Giỏi"
            elif diem_tb >= 5:
                return "Khá"
            else:
                return "Trung bình"
        return "Chưa có dữ liệu"
