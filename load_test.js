import http from 'k6/http';
import { sleep } from 'k6';


export const options = {
  vus: 10,
  duration: '90s',
  cloud: {
    // Project: rimaz
    projectID: 3706370,
    // Test runs with the same name groups test runs together.
    name: 'Test (23/07/2024-23:20:00)'
  }
};

export default function() {
  http.get('https://pumped-mite-humorous.ngrok-free.app/vote_summary');
  http.get('https://pumped-mite-humorous.ngrok-free.app/clues');
  http.get('https://pumped-mite-humorous.ngrok-free.app/detectives');
  const options = ['maha', 'richard', 'maha'];
  const selectedOption = options[Math.floor(Math.random() * options.length)];
  http.post('https://pumped-mite-humorous.ngrok-free.app/vote', JSON.stringify({ detective_id: 1, suspect: selectedOption }), {
    headers: { 'Content-Type': 'application/json' },
  });
  sleep(1);
}