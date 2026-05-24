import math

class CCBEdemaPredictor:
    def __init__(self):
        # Baseline log-odds calibrated to ~10-15% baseline hazard
        self.baseline_intercept = -2.2
        
        # Coefficients derived from Tolla et al. 2026 & high-impact meta-analyses
        self.coef_standing_long = math.log(1.92)  # Tolla et al. (AOR = 1.92)
        self.coef_high_dose = math.log(1.58)      # Tolla et al. (AOR = 1.58 trend)
        self.coef_female = math.log(1.30)         # Literature weight
        self.coef_older_age = math.log(1.40)      # Literature weight
        self.coef_raas_inhibitor = math.log(0.62) # Protective effect (OR ~ 0.60)

    def calculate_risk(self, age, gender, daily_standing_hours, ccb_dose, taking_raas_inhibitor):
        z = self.baseline_intercept
        
        if daily_standing_hours >= 3.0:
            z += self.coef_standing_long
            
        if "High" in ccb_dose:
            z += self.coef_high_dose
            
        if gender == "Female":
            z += self.coef_female
            
        if age >= 60:
            z += self.coef_older_age
            
        if taking_raas_inhibitor:
            z += self.coef_raas_inhibitor
            
        probability = 1 / (1 + math.exp(-z))
        return round(probability * 100, 1)