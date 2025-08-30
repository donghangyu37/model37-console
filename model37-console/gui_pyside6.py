import sys, threading, requests, os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8080")
API_TOKEN = os.getenv("API_TOKEN", "change_me")

class Model37GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("37号预测模型 - 桌面版")
        self.resize(920, 600)

        self.status = QLabel("准备就绪")
        self.token_input = QLineEdit(API_TOKEN); self.token_input.setEchoMode(QLineEdit.Password)
        self.addr_input = QLineEdit(API_BASE)

        btn_run = QPushButton("运行今天预测")
        btn_view = QPushButton("查看今日价值比赛")
        btn_csv = QPushButton("下载CSV到本机...")

        btn_run.clicked.connect(self.run_today)
        btn_view.clicked.connect(self.view_today)
        btn_csv.clicked.connect(self.save_csv)

        head = QHBoxLayout()
        head.addWidget(QLabel("API 地址:")); head.addWidget(self.addr_input)
        head.addWidget(QLabel("令牌:")); head.addWidget(self.token_input)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["league","home","away","market","selection","odds","prob","ev"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)

        lay = QVBoxLayout()
        lay.addLayout(head)
        lay.addWidget(btn_run)
        lay.addWidget(btn_view)
        lay.addWidget(btn_csv)
        lay.addWidget(self.status)
        lay.addWidget(self.table)
        self.setLayout(lay)

    def set_status(self, text):
        self.status.setText(text)

    def thread(self, fn):
        t = threading.Thread(target=fn, daemon=True); t.start()

    def run_today(self):
        def work():
            try:
                base = self.addr_input.text().strip()
                tok = self.token_input.text().strip()
                r = requests.post(f"{base}/run/today",
                                  headers={"Authorization": f"Bearer {tok}"}, timeout=60)
                if r.ok:
                    j = r.json()
                    self.set_status(f"已触发：筛选 {j['count']} 场；报告 {j['report']}")
                else:
                    self.set_status(f"失败：{r.status_code} {r.text}")
            except Exception as e:
                self.set_status(f"异常：{e}")
        self.thread(work)

    def view_today(self):
        def work():
            try:
                base = self.addr_input.text().strip()
                tok = self.token_input.text().strip()
                r = requests.get(f"{base}/value-picks/today",
                                 headers={"Authorization": f"Bearer {tok}"}, timeout=60)
                if r.ok:
                    rows = r.json()
                    self.table.setRowCount(len(rows))
                    cols = ["league","home","away","market","selection","odds","prob","ev"]
                    for i, row in enumerate(rows):
                        for c, k in enumerate(cols):
                            v = row.get(k, "")
                            item = QTableWidgetItem(str(v))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.table.setItem(i, c, item)
                    self.set_status(f"已加载 {len(rows)} 条。")
                else:
                    self.set_status(f"失败：{r.status_code} {r.text}")
            except Exception as e:
                self.set_status(f"异常：{e}")
        self.thread(work)

    def save_csv(self):
        base = self.addr_input.text().strip()
        tok = self.token_input.text().strip()
        path, _ = QFileDialog.getSaveFileName(self, "保存今日CSV", "today.csv", "CSV Files (*.csv)")
        if not path: return
        try:
            r = requests.get(f"{base}/report/today.csv",
                             headers={"Authorization": f"Bearer {tok}"}, timeout=60)
            if r.ok:
                with open(path, "wb") as f:
                    f.write(r.content)
                self.set_status(f"已保存到：{path}")
            else:
                self.set_status(f"失败：{r.status_code} {r.text}")
        except Exception as e:
            self.set_status(f"异常：{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Model37GUI(); w.show()
    sys.exit(app.exec())
