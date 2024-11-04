import { API_BASE_URL } from '../config';

export const fetchAnalysisData = async (params) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching analysis data:', error);
    throw error;
  }
};