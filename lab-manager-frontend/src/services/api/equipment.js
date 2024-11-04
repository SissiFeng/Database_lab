import { API_BASE_URL } from '../config';

export const fetchEquipment = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/equipment`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching equipment:', error);
    return [];
  }
};