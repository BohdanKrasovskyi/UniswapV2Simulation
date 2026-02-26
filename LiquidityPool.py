class LiquidityPool:
    """Class which simulates a Constant-Product AMM liquidity pool (x * y = k)."""


    def __init__(self, amountA: float, amountB: float, fee: float):
        """Initialize the liquidity pool with two token reserves and a swap fee.
            Args:
                amountA: Initial reserve of token A (must be > 0)
                amountB: Initial reserve of token B (must be > 0)
                fee:     Swap fee fraction, e.g. 0.003 for 0.3% (must be in [0, 1))
        """
        if amountA <= 0 or amountB <= 0:
            raise ValueError("Reserves must be positive")
        if not (0 <= fee < 1):
            raise ValueError("Fee must be between 0 and 1")

        self.amountA = amountA
        self.amountB = amountB
        self.fee = fee


    def swap(self, amountIn: float, tradeDirection: str):
        """
            Execute a swap on the pool using the constant-product formula (x * y = k).
            Args:
                amountIn:       Amount of input token to swap (must be > 0)
                tradeDirection: Swap direction — 'AtoB' or 'BtoA'
            Returns:
                dict with amountOut, newReserveA, newReserveB, effectivePrice, slippage
            """

        # Determine reserves and spot price based on swap direction.
        # reserveIn  — reserve of the token we are sending into the pool
        # reserveOut — reserve of the token we are taking out of the pool
        # spotPrice  — current price (how much reserveOut we get per 1 reserveIn) before the swap
        if amountIn <= 0:
            raise ValueError("amountIn must be > 0")

        if tradeDirection == "AtoB":
            reserveIn = self.amountA
            reserveOut = self.amountB
            spotPrice = self.amountB / self.amountA
        elif tradeDirection == "BtoA":
            reserveIn = self.amountB
            reserveOut = self.amountA
            spotPrice = self.amountA / self.amountB
        else:
            raise ValueError("tradeDirection must be 'AtoB' or 'BtoA'")

        # Prevent swaps that would drain the pool entirely
        if amountIn >= reserveIn:
            raise ValueError("amountIn too large")

        # Apply fee — the fee fraction stays in the pool as reward for LP providers
        amountInWithFee = amountIn * (1 - self.fee)

        # Constant product formula: k = reserveIn * reserveOut must hold after swap
        # amountOut = reserveOut - k / (reserveIn + amountInWithFee)
        k = reserveIn * reserveOut
        amountOut = reserveOut - (k / (reserveIn + amountInWithFee))

        # Effective price — how much reserveOut we actually received per 1 reserveIn
        effectivePrice = amountOut / amountIn

        # Slippage — difference between spot price and effective price in %
        slippage = (spotPrice - effectivePrice) / spotPrice * 100

        # Update pool reserves
        if tradeDirection == "AtoB":
            self.amountA += amountIn
            self.amountB -= amountOut
        else:
            self.amountB += amountIn
            self.amountA -= amountOut

        return {
            "amountOut": amountOut,             # Amount of output token received
            "newReserveA": self.amountA,        # Updated reserve of token A
            "newReserveB": self.amountB,        # Updated reserve of token B
            "effectivePrice": effectivePrice,   # Actual price paid per input token
            "slippage": slippage                # Loss in % caused by moving the price along the bonding curve
        }