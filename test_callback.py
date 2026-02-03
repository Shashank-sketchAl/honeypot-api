import unittest
from unittest.mock import patch, MagicMock
from callback import send_final_callback

class TestCallback(unittest.TestCase):
    
    def setUp(self):
        self.valid_session = {
            "sessionId": "test-session-123",
            "scamDetected": True,
            "totalTurns": 12,
            "riskScore": 0.85,
            "scamReasons": ["Urgency detected", "UPI request"],
            "extractedIntelligence": {
                "bankAccounts": ["123456789"],
                "upiIds": ["scam@upi"],
                "phoneNumbers": ["9876543210"],
                "phishingLinks": ["http://bad.com"]
            },
            "callbackSent": False
        }

    @patch('requests.post')
    def test_successful_callback(self, mock_post):
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        send_final_callback(self.valid_session)
        
        # Verify call arguments
        self.assertTrue(mock_post.called)
        args, kwargs = mock_post.call_args
        
        payload = kwargs['json']
        self.assertEqual(payload['sessionId'], "test-session-123")
        self.assertEqual(payload['totalMessagesExchanged'], 12)
        self.assertEqual(payload['extractedIntelligence']['upiIds'], ["scam@upi"])
        self.assertIn("Urgency detected", payload['agentNotes'])
        
        print("\n[Test] Successful callback verified.")

    @patch('requests.post')
    def test_skipped_short_conversation(self, mock_post):
        short_session = self.valid_session.copy()
        short_session['totalTurns'] = 5
        
        send_final_callback(short_session)
        
        self.assertFalse(mock_post.called)
        print("[Test] Short conversation skipped correctly.")

    @patch('requests.post')
    def test_skipped_no_scam(self, mock_post):
        benign_session = self.valid_session.copy()
        benign_session['scamDetected'] = False
        
        send_final_callback(benign_session)
        
        self.assertFalse(mock_post.called)
        print("[Test] Benign session skipped correctly.")

    @patch('requests.post')
    def test_timeout_handling(self, mock_post):
        import requests
        mock_post.side_effect = requests.exceptions.Timeout
        
        # Should not raise exception
        try:
            send_final_callback(self.valid_session)
            print("[Test] Timeout handled gracefully.")
        except Exception:
            self.fail("Timeout exception was not caught!")

if __name__ == '__main__':
    unittest.main()
