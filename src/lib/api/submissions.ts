const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Submit questionnaire answers to the backend for evaluation.
 * Sends the user's answers along with their token for authenticated processing.
 */
export async function submitQuestionnaire(
  userType: 'renter' | 'owner',
  answers: Record<string, string>,
  token: string,
) {
  const response = await fetch(`${API_BASE_URL}/questionnaire`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_type: userType, answers }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to submit questionnaire');
  }

  return response.json();
}

/**
 * Classify a property using the /classify-property endpoint.
 */
export async function classifyProperty(
  location: string,
  rent: number,
  deposit: number,
  token?: string,
) {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}/classify-property`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ location, rent, deposit }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Property classification failed');
  }

  return response.json();
}

/**
 * Submit a document (offer letter or bank statement PDF) for evaluation.
 */
export async function submitDocument(
  documentType: 'offer_letter' | 'bank_account_statement',
  file: File,
  collegeName?: string,
  token?: string,
) {
  const formData = new FormData();
  formData.append('document_type', documentType);
  formData.append('file', file);
  if (collegeName) formData.append('college_name', collegeName);

  const headers: Record<string, string> = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}/submit`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Document submission failed');
  }

  return response.json();
}
