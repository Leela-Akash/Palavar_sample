"""Scan history tracking for CloudStrike."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

HISTORY_FILE = "scan_history.json"


class ScanHistory:
    """Manages scan history persistence."""
    
    @staticmethod
    def save_scan(result: Dict) -> None:
        """
        Save scan result to history.
        
        Args:
            result: Scan result dictionary
        """
        try:
            history = ScanHistory.load_history()
            
            risk = result.get('risk', {})
            findings = result.get('findings', [])
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "security_score": risk.get('security_score', 0),
                "risk_level": risk.get('risk_level', 'Unknown'),
                "findings_count": len(findings),
                "attacks_count": len(result.get('attacks', []))
            }
            
            history.append(entry)
            
            # Keep only last 50 scans
            if len(history) > 50:
                history = history[-50:]
            
            with open(HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.info(f"Saved scan to history: {entry}")
            
        except Exception as e:
            logger.error(f"Failed to save scan history: {e}")
    
    @staticmethod
    def load_history() -> List[Dict]:
        """Load scan history from file."""
        try:
            if Path(HISTORY_FILE).exists():
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load scan history: {e}")
        
        return []
    
    @staticmethod
    def get_stats() -> Dict:
        """Get scan history statistics."""
        history = ScanHistory.load_history()
        
        if not history:
            return {
                "total_scans": 0,
                "last_scan": "Never",
                "avg_score": 0
            }
        
        last_entry = history[-1]
        avg_score = sum(s.get('security_score', 0) for s in history) / len(history)
        
        try:
            last_time = datetime.fromisoformat(last_entry['timestamp'])
            last_scan = last_time.strftime("%Y-%m-%d %H:%M")
        except:
            last_scan = "Unknown"
        
        return {
            "total_scans": len(history),
            "last_scan": last_scan,
            "avg_score": int(avg_score)
        }
