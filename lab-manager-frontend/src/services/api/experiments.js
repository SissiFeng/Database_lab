import { API_BASE_URL } from '../config';

export const fetchExperiments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/experiments`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching experiments:', error);
    return [];
  }
};

export const createExperiment = async (experimentData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/experiments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(experimentData),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error creating experiment:', error);
    throw error;
  }
};