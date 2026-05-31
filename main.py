import time
import pandas as pd
import matplotlib.pyplot as plt
from data import load_prices
from metrics import (
    compute_returns,
    compute_volatility,
    compute_cumulative_return,
    compute_var,
    compute_drawdown,
    compute_correlation,
    compute_sharpe_ratio,
    
    compute_portfolio_returns,
    compute_portfolio_es,
    compute_portfolio_volatility,
    compute_portfolio_var,
    monte_carlo_portfolio
    
)

quick = input("Do you want default value ?: y or n ").lower()

if quick == "y":
    tickers = ["AAPL", "MSFT", "TSLA"]
    weights = pd.Series([0.4,0.3,0.3], index= tickers)
else:
    print("tickers exemples: AAPL,MSFT,AMZN,GOOGL,META,TSLA ")
   
    try:
        tickers_input = input("Enter tickers separated by commas: ")
        tickers= [t.strip().upper() for t in tickers_input.split(",")]
    except:
        print("Error")
        exit()

    try:
        weights_input = input("Enter weights separated by commas: ")
        weights_list = [float(w.strip()) for w in weights_input.split(",")]

        weights =  pd.Series(weights_list, index=tickers)
    except:
        print("Error")
        exit()

    if abs(weights.sum()-1) > 1e-6:
        print("weights is not egal to 1")
        exit()
        
        
        
       


def main():
    
    A = input("Do you want to specify the number of assets ? Yes or No ").lower().strip() in ("yes", "y")
    B = input("Do you want to specify the number of portolio ? Yes or No ").lower().strip() in ("yes", "y")
    C = input("Do you want graphs? Yes or No ").lower().strip() in ("yes", "y")  
    
    start = time.time()
    
    
    
    #dataloading
    prices = load_prices(tickers)
    if prices.empty:
        print("No price data downloaded, check ticker availability.")
        return
    #assets
    
    returns = compute_returns(prices)
    if returns.empty:
        print("Not enough data to compute returns.")
        return

    volatility = compute_volatility(returns)
    cumulative_return = compute_cumulative_return(returns)
    var = compute_var(returns)
    drawdown = compute_drawdown(prices)
    corr = compute_correlation(returns)
    sharpe_ratio= compute_sharpe_ratio(returns)
    
    #portfolio
   
    portfolio_returns = compute_portfolio_returns(returns, weights)
    portfolio_es = compute_portfolio_es(portfolio_returns)
    portfolio_volatility = compute_portfolio_volatility(returns,weights)
    portfolio_var = compute_portfolio_var(portfolio_returns)
    portfolio_sharpe = compute_sharpe_ratio(portfolio_returns)
    mc_var, mc_es, mc_portfolio_returns = monte_carlo_portfolio(returns, weights)

    if A:
        print("=" * 60)
        print("RETURNS")
        print(returns)

        print("=" * 60)
        print("VOLATILITY")
        print(volatility)

        print("=" * 60)
        print("CUMULATIVE RETURN")
        print(cumulative_return)

        print("=" * 60)
        print("VAR (95%), 1 DAY")
        print(var)

        print("=" * 60)
        print("MAX DRAWDOWN")
        print(drawdown)

        print("=" * 60)
        print("CORRELATION MATRIX")
        print(corr)
        
        print("=" * 60)
        print("SHARPE RATIO")
        print(sharpe_ratio)
    
    # portfolio 
    
    
    
    if B:    
        print("=" * 60)
        print("PORTFOLIO RETURNS")
        print(portfolio_returns)

        print("=" * 60)
        print("PORTFOLIO VOLATILITY")
        print(portfolio_volatility)
        
        
        print("=" * 60)
        print("SHARPE RATIO (PORTFOLIO)")
        print(portfolio_sharpe)
        
        
        print("=" * 60)
        print("PORTFOLIO VAR (95%)")
        print(portfolio_var)

        print("=" * 60)
        print("PORTFOLIO ES (95%)")
        print(portfolio_es)
    
    
     # monte carlo 
    
    
        print("=" * 60)
        print("MONTE CARLO VAR (95%)")
        print(mc_var)

        print("=" * 60)
        print("MONTE CARLO ES (95%)")
        print(mc_es)

        print("=" * 60)
        print("MONTE CARLO SIMULATED PORTFOLIO RETURNS")
        print(mc_portfolio_returns[:10])
    
    
    
    
    end = time.time()
    print(f"\n{end - start:.3f} seconds")
    
    
    
    #graph
    
    if C:
        prices.plot()
        plt.title("Assets prices by days")
        plt.ylabel("Prices")
        plt.xlabel("Date")
        plt.grid()
    
    
    
        cumula = (1+ returns).cumprod()-1
        cumulative_portfolio = (1 + portfolio_returns).cumprod() - 1
        cumulative_portfolio.name = "Portfolio"
        comparison = pd.concat([cumula, cumulative_portfolio], axis=1)
    
        comparison.plot()
        plt.title("Cumulative Returns: Assets vs Portfolio")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.grid()
    
    
    
        plt.figure()
        mean = portfolio_returns.mean()
        portfolio_returns.hist(bins=50,color="red",edgecolor="black",label="mean")
        plt.axvline(mean,linewidth=5,color='black')
        plt.title("Distribution of Portfolio Returns")
        plt.xlabel("Returns")
        plt.ylabel("Frequency")
        plt.grid()
        
        plt.figure()
        plt.imshow(corr,cmap="plasma", vmin=-1,vmax=1)
        plt.colorbar()
        plt.xticks(range(len(corr.columns)),corr.columns)
        plt.yticks(range(len(corr.columns)), corr.columns)
    
    
    
        plt.figure()
        plt.hist(mc_portfolio_returns, bins=50, edgecolor="black")
        plt.title("Monte Carlo Portfolio Returns")
        plt.xlabel("Simulated Return")
        plt.ylabel("Frequency")
        plt.grid()
        
        plt.show()
    
    
    
if __name__ == "__main__":
    main()


