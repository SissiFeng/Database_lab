import { API_BASE_URL } from '../config';

export const deployToPrefect = async (flowData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/workflows/deploy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        flow_name: flowData.name,
        tasks: flowData.nodes.map(node => ({
          task_name: node.id,
          task_type: node.type,
          parameters: node.data.parameters,
          upstream_tasks: flowData.edges
            .filter(edge => edge.target === node.id)
            .map(edge => edge.source)
        }))
      })
    });
    return await response.json();
  } catch (error) {
    console.error('Error deploying to Prefect:', error);
    throw error;
  }
};
