"""
Rule-Based Inference Engine for Program Recommendation
"""

import json
from typing import Dict, List, Any


class InferenceEngine:
    """
    Forward-chaining rule-based inference engine for program recommendation
    """
    
    def __init__(self, db):
        self.db = db
    
    def generate_recommendations(self, student_profile: Dict, response_id: int) -> List[Dict]:
        """
        Main recommendation generation function
        
        Args:
            student_profile: Dictionary containing student questionnaire data
            response_id: ID of the questionnaire response
            
        Returns:
            List of recommendations sorted by confidence score
        """
        from models import Rule
        
        # Load all active rules
        rules = Rule.query.filter_by(is_active=True).all()
        
        # Fire rules and collect recommendations
        fired_recommendations = []
        
        for rule in rules:
            result = self.evaluate_rule(rule, student_profile)
            if result:
                fired_recommendations.append(result)
        
        # Aggregate recommendations for same programs
        aggregated = self.aggregate_recommendations(fired_recommendations)
        
        # Rank by confidence score
        ranked = self.rank_recommendations(aggregated)
        
        # Return top 5
        return ranked[:5]
    
    from typing import Optional
    def evaluate_rule(self, rule, student_profile: Dict) -> Optional[Dict]:
        """
        Evaluate a single rule against student profile
        
        Args:
            rule: Rule object from database
            student_profile: Student questionnaire data
            
        Returns:
            Recommendation dict if rule fires, None otherwise
        """
        try:
            # Parse rule conditions
            conditions = json.loads(rule.conditions)
            
            # Evaluate conditions
            if self.evaluate_conditions(conditions, student_profile):
                return {
                    'program_id': rule.recommended_program_id,
                    'confidence': float(rule.confidence_score),
                    'justification': rule.justification,
                    'rule_id': rule.rule_id
                }
            
            return None
            
        except Exception as e:
            print(f"Error evaluating rule {rule.rule_id}: {e}")
            return None
    
    def evaluate_conditions(self, conditions: Dict, profile: Dict) -> bool:
        """
        Recursively evaluate rule conditions
        
        Args:
            conditions: Dictionary with operator and criteria
            profile: Student profile data
            
        Returns:
            True if conditions are met, False otherwise
        """
        operator = conditions.get('operator', 'AND')
        criteria = conditions.get('criteria', [])
        
        results = []
        
        for criterion in criteria:
            field = criterion['field']
            cond_operator = criterion['operator']
            expected_value = criterion['value']
            
            # Get actual value from profile
            actual_value = self.get_nested_value(profile, field)
            
            # Evaluate based on operator
            if cond_operator == '==':
                results.append(actual_value == expected_value)
            elif cond_operator == '>=':
                results.append(float(actual_value) >= float(expected_value))
            elif cond_operator == '<=':
                results.append(float(actual_value) <= float(expected_value))
            elif cond_operator == 'IN':
                if isinstance(expected_value, list):
                    results.append(actual_value in expected_value)
                else:
                    results.append(False)
            elif cond_operator == 'CONTAINS':
                if isinstance(actual_value, list):
                    results.append(expected_value in actual_value)
                elif isinstance(actual_value, str):
                    # Handle JSON string
                    try:
                        actual_list = json.loads(actual_value) if isinstance(actual_value, str) else actual_value
                        results.append(expected_value in actual_list)
                    except:
                        results.append(False)
                else:
                    results.append(False)
            else:
                results.append(False)
        
        # Apply logical operator
        if operator == 'AND':
            return all(results) if results else False
        elif operator == 'OR':
            return any(results) if results else False
        else:
            return False
    
    def get_nested_value(self, data: Dict, field: str) -> Any:
        """
        Get value from nested dictionary using dot notation
        
        Args:
            data: Dictionary to search
            field: Field name, supports dot notation (e.g., 'skills.analytical')
            
        Returns:
            Value if found, None otherwise
        """
        keys = field.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
            
            if value is None:
                return None
        
        return value
    
    def aggregate_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Aggregate recommendations for the same program
        
        Args:
            recommendations: List of fired rule recommendations
            
        Returns:
            Aggregated list with combined confidence and justifications
        """
        program_map = {}
        
        for rec in recommendations:
            program_id = rec['program_id']
            
            if program_id in program_map:
                # Combine confidence scores (weighted average)
                existing = program_map[program_id]
                total_confidence = existing['confidence'] + rec['confidence']
                avg_confidence = total_confidence / 2
                
                program_map[program_id]['confidence'] = avg_confidence
                program_map[program_id]['rules_triggered'].append(rec['rule_id'])
                
                # Combine justifications
                if rec['justification'] not in existing['justification']:
                    program_map[program_id]['justification'] += f" Additionally, {rec['justification']}"
            else:
                program_map[program_id] = {
                    'program_id': program_id,
                    'confidence': rec['confidence'],
                    'justification': rec['justification'],
                    'rules_triggered': [rec['rule_id']]
                }
        
        return list(program_map.values())
    
    def rank_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Rank recommendations by confidence score
        
        Args:
            recommendations: List of recommendations
            
        Returns:
            Sorted list with rank positions added
        """
        # Sort by confidence (descending)
        sorted_recs = sorted(recommendations, key=lambda x: x['confidence'], reverse=True)
        
        # Add rank position
        for idx, rec in enumerate(sorted_recs):
            rec['rank'] = idx + 1
        
        return sorted_recs


# ============================================
# HELPER FUNCTIONS FOR RULE CREATION
# ============================================

def create_rule_condition(operator='AND', criteria=None):
    """
    Helper function to create rule condition JSON
    
    Args:
        operator: 'AND' or 'OR'
        criteria: List of criterion dictionaries
        
    Returns:
        JSON string of condition structure
    """
    if criteria is None:
        criteria = []
    
    condition = {
        'operator': operator,
        'criteria': criteria
    }
    
    return json.dumps(condition)


def create_criterion(field, operator, value):
    """
    Helper function to create a single criterion
    
    Args:
        field: Field name (supports dot notation)
        operator: Comparison operator (==, >=, <=, IN, CONTAINS)
        value: Expected value
        
    Returns:
        Criterion dictionary
    """
    return {
        'field': field,
        'operator': operator,
        'value': value
    }


# Example usage:
"""
# Create a rule for STEM students interested in technology
criteria = [
    create_criterion('strand', '==', 'STEM'),
    create_criterion('interests', 'CONTAINS', 'Technology'),
    create_criterion('skills.analytical', '>=', 4)
]

condition_json = create_rule_condition('AND', criteria)

# This can be stored in the Rule table's conditions field
"""
