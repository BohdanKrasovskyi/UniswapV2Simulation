import matplotlib.pyplot as plt
from LiquidityPool import LiquidityPool

# Initial pool reserves and swap parameters
amountA = 1000
amountB = 1000
fee = 0.003
tradeDirection = "AtoB"

results = []

# Simulate swaps from 1 to 50% of reserveA.
# Each iteration creates a fresh pool so swaps are independent (no state carryover).
# amountIn is normalized to [0, 1] to show trade size as a fraction of the pool.
for amountIn in range(1, amountA // 2):
    liquidityPool = LiquidityPool(amountA, amountB, fee)
    params = liquidityPool.swap(amountIn, tradeDirection)
    results.append([amountIn / amountA * 100, params.get("slippage")])

x = [r[0] for r in results] # Trade size as fraction of reserveA
y = [r[1] for r in results] # Resulting slippage in %

# Visualize the relationship between trade size (as % of pool) and slippage
plt.figure(figsize=(10, 6))
plt.plot(x, y, color="royalblue", linewidth=2)
plt.title("Slippage vs Trade Size", fontsize=14)
plt.xlabel("amountIn as % of pool", fontsize=12)
plt.ylabel("Slippage (%)", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

liquidityPool = LiquidityPool(amountA, amountB, fee)
print(liquidityPool.swap(amountA / 100, tradeDirection)) #1% of pool
liquidityPool = LiquidityPool(amountA, amountB, fee)
print(liquidityPool.swap(amountA / 10, tradeDirection))  #10% of pool
liquidityPool = LiquidityPool(amountA, amountB, fee)
print(liquidityPool.swap(amountA / 2.5 , tradeDirection))  #40$ of pool