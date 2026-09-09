import sys
with open("index.html", "r") as f:
    content = f.read()

target = """              <!-- Metrics Section: 2 Columns Box matching Image 2 -->"""
replacement = """              <!-- HNWI Dual Option Strategy Box -->
              ${item.hnwi_strategy && item.hnwi_strategy.has_dual_option && html`
                <div className="mt-5 mb-2 rounded-2xl border-2 border-emerald-500/30 bg-emerald-50/50 p-4">
                  <div className="flex items-center gap-2 mb-3 pb-2 border-b border-emerald-200">
                    <strong className="text-xs font-black uppercase tracking-wider text-emerald-900">
                      🎯 CHIẾN LƯỢC KÉP DÀNH CHO KHÁCH HÀNG VIP (Vốn khả dụng > Giá trị tài sản)
                    </strong>
                  </div>
                  <div className="grid md:grid-cols-2 gap-3 text-xs leading-relaxed">
                    <div className="rounded-xl bg-white p-3 border border-emerald-200/80 shadow-sm">
                      <span className="text-[10px] font-black uppercase tracking-wider text-emerald-800 block mb-1">
                        KỊCH BẢN 1: THANH TOÁN SỚM 100%
                      </span>
                      <p className="text-ink/80 font-medium mb-1">
                        Thanh toán đứt không cần vay, an toàn tuyệt đối. Nhận chiết khấu tối đa từ CĐT (nếu có).
                      </p>
                      <strong className="text-emerald-700">Dư tiền mặt: ${(item.hnwi_strategy.outright_cash_left / 1e9).toFixed(1)} Tỷ</strong>
                    </div>

                    <div className="rounded-xl bg-white p-3 border border-amber-200/80 shadow-sm">
                      <span className="text-[10px] font-black uppercase tracking-wider text-amber-800 block mb-1">
                        KỊCH BẢN 2: ĐÒN BẨY (GÓI HTLS)
                      </span>
                      <p className="text-ink/80 font-medium mb-1">
                        Vay 70% ân hạn gốc lãi. Mang tiền đi đầu tư kênh khác (chứng khoán, KD) để bù đắp lãi thả nổi.
                      </p>
                      <strong className="text-amber-700">Dư tiền mặt: ${(item.hnwi_strategy.leverage_cash_left / 1e9).toFixed(1)} Tỷ</strong>
                    </div>
                  </div>
                </div>
              `}

              <!-- Metrics Section: 2 Columns Box matching Image 2 -->"""

if target in content:
    content = content.replace(target, replacement)
    with open("index.html", "w") as f:
        f.write(content)
    print("PATCH UI HNWI SUCCESSFUL")
else:
    print("TARGET NOT FOUND")
