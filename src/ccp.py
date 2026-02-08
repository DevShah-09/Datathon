import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CCP:
    def __init__(self):
        self.default_margin = 0.10 # 10%
        self.current_margin = 0.10
        self.cash_waterfall = 50000 # $50B in reserve
        self.ai_mode = False
        self.active_contracts = 0
        self.allotment_log = [] # Detailed history of fund management events

    def set_mode(self, ai_enabled: bool):
        self.ai_mode = ai_enabled

    def calculate_margin(self, ai_health_score, price_trend):
        """
        Policy Decision Logic:
        1. Conservative Mode: Health > 7 & Stable LSTM -> 10% Margin
        2. Caution Mode: Health 4-7 -> 25% Margin
        3. Crisis Mode: Health < 4 or LSTM Spike (-15%) -> 50% Margin
        """
        if self.ai_mode:
            if ai_health_score < 4 or price_trend < -0.15:
                self.current_margin = 0.50 # Crisis Threshold
                logger.info("CCP: CRISIS MODE - Margins raised to 50%.")
            elif ai_health_score < 7:
                self.current_margin = 0.25 # Caution
            else:
                self.current_margin = 0.10 # Conservative
        else:
            # Fallback to pure price trend
            self.current_margin = 0.20 if price_trend < -0.10 else 0.10
            
        return self.current_margin

    def perform_novation(self, num_trades):
        """
        The "Novation" Process:
        Step 1: Original bilateral contracts between Bank A and Bank B are 'deleted' from private ledgers.
        Step 2: CCP steps in as the central buyer to every seller and seller to every buyer.
        Step 3: Original contract is replaced by (Bank A <-> CCP) and (CCP <-> Bank B).
        Result: If Bank A fails, Bank B's contract remains valid with the CCP.
        """
        # Simulated Novation: The CCP takes over twice the number of original trade legs
        self.active_contracts += (num_trades * 2)
        logger.info(f"CCP: Novation complete for {num_trades} trades. {num_trades*2} new centralised contracts created.")
        return num_trades * 2

    def process_failures(self, failed_bank_name, connected_banks, loss_per_bank):
        """
        Detailed Loss Absorption & Allotment:
        Tracks exactly how much of the cash waterfall protected each connected counterparty.
        """
        events = []
        total_loss = sum(loss_per_bank.values())
        
        absorbed_total = 0
        if self.cash_waterfall > 0:
            for bank, loss in loss_per_bank.items():
                if self.cash_waterfall <= 0: break
                
                # Check if we can cover this bank's entire hit
                coverage = min(loss, self.cash_waterfall)
                self.cash_waterfall -= coverage
                absorbed_total += coverage
                
                event = {
                    'target_bank': bank,
                    'failed_bank': failed_bank_name,
                    'allotment': coverage,
                    'status': 'Fully Protected' if coverage >= loss else 'Partially Absorbed'
                }
                self.allotment_log.append(event)
                events.append(event)
                
            logger.info(f"CCP: Absorbed ${absorbed_total:.1f}M across {len(events)} connected banks.")
        
        return {
            'success': absorbed_total >= total_loss,
            'absorbed': absorbed_total,
            'remaining_loss': max(0, total_loss - absorbed_total),
            'detailed_events': events
        }
