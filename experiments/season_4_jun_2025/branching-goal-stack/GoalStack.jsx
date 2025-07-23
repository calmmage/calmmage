import React, {useEffect, useState} from 'react';
import {ArrowUp, Clock, Menu, MessageSquare, Plus, Target, X} from 'lucide-react';

// Simple markdown-to-JSX converter
const parseMarkdown = (text) => {
  if (!text) return text;
  
  // Split by lines first to preserve line breaks
  const lines = text.split('\n');
  const elements = [];
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    
    // Skip empty lines but add spacing
    if (line.trim() === '') {
      elements.push(<br key={`br-${i}`} />);
      continue;
    }
    
    // Process inline formatting
    const parts = [];
    let lastIndex = 0;
    
    // Bold text
    line = line.replace(/\*\*(.*?)\*\*/g, (match, content, offset) => {
      if (offset > lastIndex) {
        parts.push(line.slice(lastIndex, offset));
      }
      parts.push(<strong key={`bold-${offset}`}>{content}</strong>);
      lastIndex = offset + match.length;
      return '';
    });
    
    // Add remaining text
    if (lastIndex < line.length) {
      parts.push(line.slice(lastIndex));
    }
    
    // Check for list items
    if (line.trim().match(/^[-*•]\s/)) {
      elements.push(
        <div key={`line-${i}`} className="ml-4 mb-1">
          <span className="text-gray-600 mr-2">•</span>
          {parts.length > 0 ? parts : line.replace(/^[-*•]\s/, '')}
        </div>
      );
    } else {
      elements.push(
        <div key={`line-${i}`} className="mb-1">
          {parts.length > 0 ? parts : line}
        </div>
      );
    }
  }
  
  return <div>{elements}</div>;
// Chat History Sidebar Component
const ChatHistorySidebar = ({ isOpen, onClose, savedChats, onLoadChat, onDeleteChat }) => {
  if (!isOpen) return null;

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  const getChatPreview = (workspaces) => {
    if (!workspaces || workspaces.length === 0) return 'Empty chat';
    const firstWorkspace = workspaces[0];
    const userMessages = firstWorkspace.messages.filter(m => m.type === 'user');
    if (userMessages.length === 0) return firstWorkspace.goal || 'New chat';
    return userMessages[0].content.slice(0, 50) + (userMessages[0].content.length > 50 ? '...' : '');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex">
      <div className="bg-white w-80 h-full shadow-xl flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-800">Chat History</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Chat List */}
        <div className="flex-1 overflow-y-auto">
          {savedChats.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <MessageSquare className="w-12 h-12 mx-auto mb-2 text-gray-300" />
              <p>No saved chats yet</p>
              <p className="text-sm">Start chatting to see your history here</p>
            </div>
          ) : (
            <div className="p-2">
              {savedChats.map((chat) => (
                <div
                  key={chat.id}
                  className="p-3 mb-2 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => {
                    onLoadChat(chat);
                    onClose();
                  }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-medium text-gray-800 text-sm mb-1">
                        {chat.workspaces && chat.workspaces.length > 0 && chat.workspaces[0].goal 
                          ? chat.workspaces[0].goal 
                          : 'Untitled Chat'}
                      </div>
                      <div className="text-xs text-gray-500 mb-1">
                        {chat.workspaces?.length || 0} workspace{(chat.workspaces?.length || 0) !== 1 ? 's' : ''}
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteChat(chat.id);
                      }}
                      className="p-1 hover:bg-red-100 rounded text-red-500 hover:text-red-700 transition-colors"
                      title="Delete chat"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">
                    {getChatPreview(chat.workspaces)}
                  </div>
                  <div className="flex items-center text-xs text-gray-400">
                    <Clock className="w-3 h-3 mr-1" />
                    {formatDate(chat.timestamp)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Click outside to close */}
      <div className="flex-1" onClick={onClose}></div>
    </div>
  );
};

// Individual workspace component
const Workspace = ({ goal, isActive, depth, onDiveDeeper, messages, onSendMessage, newMessage, onMessageChange, onGoalEdit, onBranchConversation, streaming, detectedSubGoals }) => {
  const isCollapsed = !isActive;
  
  return (
    <div 
      className={`workspace absolute top-0 h-full bg-white border-r border-gray-200 transition-all duration-500 ease-in-out ${
        isCollapsed ? 'w-16 shadow-lg' : 'w-full'
      }`}
      style={{
        left: `${depth * 64}px`,
        zIndex: 10 - depth
      }}
    >
      {/* Collapsed View */}
      {isCollapsed && (
        <div className="h-full flex flex-col items-center py-4 bg-gray-50">
          <Target className="w-6 h-6 text-gray-600 mb-2" />
          <div className="writing-mode-vertical text-xs text-gray-600 px-2 text-center line-clamp-3">
            {goal ? goal.substring(0, 20) + '...' : 'New Goal'}
          </div>
        </div>
      )}
      
      {/* Active View */}
      {!isCollapsed && (
        <div className="h-full flex flex-col">
          {/* Goal Header - Always Pinned */}
          <GoalHeader 
            goal={goal} 
            depth={depth} 
            onGoalEdit={(newGoal) => onGoalEdit && onGoalEdit(newGoal)}
          />
          
          {/* Chat Interface */}
          <ChatInterface 
            messages={messages}
            onSendMessage={onSendMessage}
            newMessage={newMessage}
            onMessageChange={onMessageChange}
            onBranchConversation={onBranchConversation}
            streaming={streaming}
            detectedSubGoals={detectedSubGoals}
            goal={goal}
          />
        </div>
      )}
    </div>
  );
};

// Fixed goal header component
const GoalHeader = ({ goal, depth, onGoalEdit }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(goal || '');

  const handleGoalSave = () => {
    if (editText.trim()) {
      onGoalEdit(editText.trim());
      setIsEditing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGoalSave();
    } else if (e.key === 'Escape') {
      setEditText(goal || '');
      setIsEditing(false);
    }
  };

  return (
    <div className="goal-header bg-blue-50 border-b border-blue-200 p-4 flex items-center gap-3">
      <Target className="w-5 h-5 text-blue-600" />
      <div className="flex-1">
        <div className="text-sm text-blue-600 font-medium">Goal {depth + 1}</div>
        {isEditing ? (
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            onBlur={handleGoalSave}
            onKeyDown={handleKeyPress}
            className="w-full mt-1 px-2 py-1 border border-blue-300 rounded text-gray-800 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
        ) : (
          <div 
            className="text-gray-800 font-medium cursor-pointer hover:text-blue-600 transition-colors"
            onClick={() => setIsEditing(true)}
            title="Click to edit goal"
          >
            {goal || 'Click to set your goal...'}
          </div>
        )}
      </div>
    </div>
  );
};

// Chat interface component
const ChatInterface = ({ messages, onSendMessage, newMessage, onMessageChange, onBranchConversation, streaming, detectedSubGoals, goal }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Shift+Enter creates new line - let default behavior happen
        return;
      } else if (e.metaKey || e.ctrlKey) {
        // Cmd+Enter (Mac) or Ctrl+Enter (PC) branches conversation
        e.preventDefault();
        onBranchConversation();
      } else if (!streaming) {
        // Regular Enter sends message
        e.preventDefault();
        onSendMessage();
      }
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, idx) => (
          <div key={idx} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              message.type === 'user' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-800'
            } ${message.streaming ? 'animate-pulse' : ''}`}>
              {message.type === 'user' ? (
                // User messages: preserve line breaks with white-space
                <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
              ) : (
                // AI messages: parse markdown and format properly
                <div>
                  {parseMarkdown(message.content)}
                  {message.streaming && <span className="inline-block w-2 h-5 bg-gray-400 ml-1 animate-pulse">|</span>}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Sub-goal Detection Results */}
        {detectedSubGoals && detectedSubGoals.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="text-sm font-medium text-yellow-800 mb-2">🌿 Potential sub-goals detected:</div>
            {detectedSubGoals.map((subGoal, idx) => (
              <div key={idx} className="mb-2 last:mb-0">
                <div className="text-xs text-yellow-700 mb-1">"{subGoal.text}"</div>
                <button
                  onClick={() => onBranchConversation(subGoal.suggestedGoal)}
                  className="text-xs px-2 py-1 bg-yellow-200 hover:bg-yellow-300 text-yellow-800 rounded"
                >
                  Branch: {subGoal.suggestedGoal}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Input Area */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex gap-2">
          <textarea
            value={newMessage}
            onChange={(e) => onMessageChange(e.target.value)}
            placeholder={goal ? "Type your message..." : "What would you like to work on today?"}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            onKeyDown={handleKeyPress}
            disabled={streaming}
            rows={1}
            style={{ minHeight: '38px', maxHeight: '120px' }}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
            }}
          />
          <button
            onClick={() => onSendMessage()}
            disabled={streaming || !newMessage.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
            title="Send message"
          >
            <ArrowUp className="w-4 h-4" />
          </button>
          <button
            onClick={() => onBranchConversation()}
            disabled={streaming}
            className="px-3 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:bg-gray-400"
            title="Branch conversation (⌘+Enter)"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
        <div className="text-xs text-gray-500 mt-1">
          {goal ? "Enter to send • Shift+Enter for new line • ⌘+Enter to branch" : "Enter to send • Shift+Enter for new line • ⌘+Enter to branch"}
        </div>
      </div>
    </div>
  );
};

// Main goal stack container
const GoalStack = () => {
  const [workspaces, setWorkspaces] = useState([
    {
      id: 1,
      goal: "",
      messages: [
        { type: 'assistant', content: 'Hi! What would you like to work on today?' }
      ],
      newMessage: '',
      loading: false,
      streaming: false
    }
  ]);
  
  const [activeWorkspaceId, setActiveWorkspaceId] = useState(1);
  const [showGoalInput, setShowGoalInput] = useState(false);
  const [newGoalText, setNewGoalText] = useState('');
  const [showChatHistory, setShowChatHistory] = useState(false);
  const [savedChats, setSavedChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);

  // Load saved chats on component mount
  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem('goalstack-chats') || '[]');
    setSavedChats(saved);
  }, []);

  // Auto-save current chat whenever workspaces change
  useEffect(() => {
    if (workspaces.length > 0 && workspaces.some(w => w.messages.length > 1)) {
      saveCurrentChat();
    }
  }, [workspaces]);

  const saveCurrentChat = () => {
    const chatToSave = {
      id: currentChatId || Date.now(),
      timestamp: Date.now(),
      workspaces: workspaces.map(w => ({
        ...w,
        streaming: false // Don't save streaming state
      })),
      activeWorkspaceId
    };

    const saved = JSON.parse(localStorage.getItem('goalstack-chats') || '[]');
    const existingIndex = saved.findIndex(chat => chat.id === chatToSave.id);
    
    if (existingIndex >= 0) {
      saved[existingIndex] = chatToSave;
    } else {
      saved.unshift(chatToSave);
      setCurrentChatId(chatToSave.id);
    }
    
    // Keep only last 50 chats
    const trimmed = saved.slice(0, 50);
    localStorage.setItem('goalstack-chats', JSON.stringify(trimmed));
    setSavedChats(trimmed);
  };

  const loadChat = (chat) => {
    setWorkspaces(chat.workspaces);
    setActiveWorkspaceId(chat.activeWorkspaceId);
    setCurrentChatId(chat.id);
  };

  const deleteChat = (chatId) => {
    const saved = JSON.parse(localStorage.getItem('goalstack-chats') || '[]');
    const filtered = saved.filter(chat => chat.id !== chatId);
    localStorage.setItem('goalstack-chats', JSON.stringify(filtered));
    setSavedChats(filtered);
  };

  const startNewChat = () => {
    setWorkspaces([{
      id: Date.now(),
      goal: "",
      messages: [
        { type: 'assistant', content: 'Hi! What would you like to work on today?' }
      ],
      newMessage: '',
      loading: false,
      streaming: false
    }]);
    setActiveWorkspaceId(Date.now());
    setCurrentChatId(null);
  };

  const handleSendMessage = async (workspaceId) => {
    const workspace = workspaces.find(w => w.id === workspaceId);
    if (!workspace.newMessage.trim()) return;

    const userMessage = workspace.newMessage.trim();
    
    // Auto-generate goal from first message if no goal is set
    if (!workspace.goal) {
      // Extract goal from first message using Claude
      try {
        const goalPrompt = `Based on this user message, extract or generate a concise goal/task title (max 50 characters):

User message: "${userMessage}"

Respond with a JSON object:
{
  "goal": "concise goal title"
}

Your entire response MUST be a single, valid JSON object.`;

        const goalResponse = await window.claude.complete(goalPrompt);
        const goalData = JSON.parse(goalResponse);
        
        // Update workspace with auto-generated goal
        setWorkspaces(prev => prev.map(w => 
          w.id === workspaceId 
            ? { ...w, goal: goalData.goal }
            : w
        ));
        
        // Continue with normal message processing
      } catch (error) {
        console.error('Error generating goal:', error);
        // Fallback: use first few words of message as goal
        const fallbackGoal = userMessage.split(' ').slice(0, 6).join(' ');
        setWorkspaces(prev => prev.map(w => 
          w.id === workspaceId 
            ? { ...w, goal: fallbackGoal }
            : w
        ));
      }
    }
    
    // Add user message immediately
    setWorkspaces(prev => prev.map(w => 
      w.id === workspaceId 
        ? {
            ...w,
            messages: [
              ...w.messages,
              { type: 'user', content: userMessage }
            ],
            newMessage: '',
            streaming: true
          }
        : w
    ));

    try {
      // Build conversation context for Claude
      const conversationHistory = workspace.messages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));
      
      // Add the new user message
      conversationHistory.push({
        role: 'user',
        content: userMessage
      });

      // Create prompt with goal context
      const goalContext = workspace.goal ? `You are helping someone work on their goal: "${workspace.goal}"` : 'You are a productivity assistant helping someone organize their work.';
      
      const prompt = `${goalContext}

The following is the COMPLETE conversation history:
${JSON.stringify(conversationHistory)}

IMPORTANT: 
- You are a productivity assistant focused on helping achieve goals and tasks
- Consider the ENTIRE conversation history when responding
- Be concise but helpful and actionable
- If you mention sub-tasks, blockers, or related topics, be specific about them
- Your response should be practical and move the conversation forward

Respond with a JSON object in this format:
{
  "response": "Your helpful response considering the full conversation and goal context"
}

Your entire response MUST be a single, valid JSON object. DO NOT include anything outside the JSON.`;

      console.log('Sending prompt to Claude:', prompt);
      
      // Simulate streaming by adding the message immediately and then updating
      setWorkspaces(prev => prev.map(w => 
        w.id === workspaceId 
          ? {
              ...w,
              messages: [
                ...w.messages,
                { type: 'assistant', content: '', streaming: true }
              ]
            }
          : w
      ));
      
      const response = await window.claude.complete(prompt);
      console.log('Claude response:', response);
      
      const parsedResponse = JSON.parse(response);
      
      // Simulate streaming effect
      const fullResponse = parsedResponse.response;
      const words = fullResponse.split(' ');
      let currentText = '';
      
      for (let i = 0; i < words.length; i++) {
        currentText += (i > 0 ? ' ' : '') + words[i];
        
        setWorkspaces(prev => prev.map(w => 
          w.id === workspaceId 
            ? {
                ...w,
                messages: w.messages.map((msg, idx) => 
                  idx === w.messages.length - 1 && msg.streaming
                    ? { ...msg, content: currentText }
                    : msg
                ),
                streaming: i < words.length - 1
              }
            : w
        ));
        
        // Small delay for streaming effect
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      
      // Finalize streaming
      setWorkspaces(prev => prev.map(w => 
        w.id === workspaceId 
          ? {
              ...w,
              messages: w.messages.map(msg => ({ ...msg, streaming: false })),
              streaming: false
            }
          : w
      ));
      
      // Optional: Analyze for sub-goals in background (removed to reduce delay)
      // analyzeForSubGoals(workspaceId, userMessage, fullResponse);
      
    } catch (error) {
      console.error('Error getting Claude response:', error);
      
      // Add error message
      setWorkspaces(prev => prev.map(w => 
        w.id === workspaceId 
          ? {
              ...w,
              messages: [
                ...w.messages,
                { type: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
              ],
              streaming: false
            }
          : w
      ));
    }
  };

  const handleMessageChange = (workspaceId, message) => {
    setWorkspaces(prev => prev.map(w => 
      w.id === workspaceId ? { ...w, newMessage: message } : w
    ));
  };

  const analyzeForSubGoals = async (workspaceId, userMessage, assistantMessage) => {
    try {
      const prompt = `Analyze the following conversation exchange for potential sub-goals, sub-tasks, or topics that could be branched into separate focused discussions:

User message: "${userMessage}"
Assistant response: "${assistantMessage}"

Look for:
- Specific tasks or sub-tasks mentioned
- Blockers or challenges that need separate focus
- Topics that could benefit from dedicated attention
- Action items that are complex enough to warrant their own discussion

Respond with a JSON object:
{
  "subGoals": [
    {
      "text": "exact text from the conversation that suggests the sub-goal",
      "suggestedGoal": "suggested goal title for branching",
      "relevance": "high|medium|low"
    }
  ]
}

Only include sub-goals with "high" or "medium" relevance. If no significant sub-goals are found, return an empty array.

Your entire response MUST be a single, valid JSON object.`;

      const response = await window.claude.complete(prompt);
      const analysis = JSON.parse(response);
      
      if (analysis.subGoals && analysis.subGoals.length > 0) {
        setWorkspaces(prev => prev.map(w => 
          w.id === workspaceId 
            ? {
                ...w,
                detectedSubGoals: analysis.subGoals
              }
            : w
        ));
      }
    } catch (error) {
      console.error('Error analyzing sub-goals:', error);
    }
  };

  const handleGoalEdit = (workspaceId, newGoal) => {
    setWorkspaces(prev => prev.map(w => 
      w.id === workspaceId ? { ...w, goal: newGoal } : w
    ));
  };

  const handleBranchConversation = (workspaceId, suggestedGoal = '') => {
    setNewGoalText(suggestedGoal);
    setShowGoalInput(true);
  };

  const createNewWorkspace = () => {
    if (!newGoalText || newGoalText.trim() === '') return;

    const newWorkspace = {
      id: Date.now(),
      goal: newGoalText.trim(),
      messages: [
        { type: 'assistant', content: `Great! Let's focus on: "${newGoalText.trim()}". How can I help you with this?` }
      ],
      newMessage: '',
      streaming: false
    };

    console.log('Creating new workspace:', newWorkspace);
    setWorkspaces(prev => {
      const updated = [...prev, newWorkspace];
      console.log('Updated workspaces:', updated);
      return updated;
    });
    setActiveWorkspaceId(newWorkspace.id);
    setShowGoalInput(false);
    setNewGoalText('');
  };

  const handleWorkspaceClick = (workspaceId) => {
    setActiveWorkspaceId(workspaceId);
  };

  return (
    <div className="goal-stack h-screen bg-gray-100 relative overflow-hidden">
      {/* Top Menu Bar */}
      <div className="absolute top-0 left-0 right-0 bg-white border-b border-gray-200 px-4 py-2 flex items-center justify-between z-30">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowChatHistory(true)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Chat History"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
          <span className="text-sm font-medium text-gray-700">Goal Stack</span>
        </div>
        <button
          onClick={startNewChat}
          className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
        >
          New Chat
        </button>
      </div>

      {/* Workspace Stack - offset by menu bar */}
      <div className="pt-12 h-full">
        {workspaces.map((workspace, index) => (
          <Workspace
            key={workspace.id}
            goal={workspace.goal}
            isActive={workspace.id === activeWorkspaceId}
            depth={index}
            messages={workspace.messages}
            newMessage={workspace.newMessage}
            onSendMessage={() => handleSendMessage(workspace.id)}
            onMessageChange={(message) => handleMessageChange(workspace.id, message)}
            onGoalEdit={(newGoal) => handleGoalEdit(workspace.id, newGoal)}
            onBranchConversation={(suggestedGoal) => handleBranchConversation(workspace.id, suggestedGoal)}
            streaming={workspace.streaming}
            detectedSubGoals={workspace.detectedSubGoals}
          />
        ))}
      </div>
  return (
    <div className="goal-stack h-screen bg-gray-100 relative overflow-hidden">
      {/* Top Menu Bar */}
      <div className="absolute top-0 left-0 right-0 bg-white border-b border-gray-200 px-4 py-2 flex items-center justify-between z-30">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowChatHistory(true)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Chat History"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
          <span className="text-sm font-medium text-gray-700">Goal Stack</span>
        </div>
        <button
          onClick={startNewChat}
          className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
        >
          New Chat
        </button>
      </div>

      {/* Workspace Stack - offset by menu bar */}
      <div className="pt-12 h-full">
        {workspaces.map((workspace, index) => (
          <Workspace
            key={workspace.id}
            goal={workspace.goal}
            isActive={workspace.id === activeWorkspaceId}
            depth={index}
            messages={workspace.messages}
            newMessage={workspace.newMessage}
            onSendMessage={() => handleSendMessage(workspace.id)}
            onMessageChange={(message) => handleMessageChange(workspace.id, message)}
            onGoalEdit={(newGoal) => handleGoalEdit(workspace.id, newGoal)}
            onBranchConversation={(suggestedGoal) => handleBranchConversation(workspace.id, suggestedGoal)}
            streaming={workspace.streaming}
            detectedSubGoals={workspace.detectedSubGoals}
          />
        ))}
      </div>
      
      {/* Click handlers for collapsed workspaces */}
      <div className="pt-12 h-full">
        {workspaces.map((workspace, index) => (
          workspace.id !== activeWorkspaceId && (
            <div
              key={`click-${workspace.id}`}
              className="absolute top-12 h-full w-16 cursor-pointer"
              style={{ left: `${index * 64}px`, zIndex: 20 }}
              onClick={() => handleWorkspaceClick(workspace.id)}
            />
          )
        ))}
      </div>
      
      {/* Chat History Sidebar */}
      <ChatHistorySidebar
        isOpen={showChatHistory}
        onClose={() => setShowChatHistory(false)}
        savedChats={savedChats}
        onLoadChat={loadChat}
        onDeleteChat={deleteChat}
      />
      
      {/* Goal Input Modal */}
      {showGoalInput && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Branch Conversation</h3>
            <p className="text-sm text-gray-600 mb-4">Create a new focused workspace for a sub-goal or related topic:</p>
            <input
              type="text"
              value={newGoalText}
              onChange={(e) => setNewGoalText(e.target.value)}
              placeholder="What do you want to focus on?"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
              onKeyPress={(e) => e.key === 'Enter' && createNewWorkspace()}
              autoFocus
            />
            <div className="flex gap-2 justify-end">
              <button
                onClick={() => setShowGoalInput(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={createNewWorkspace}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Branch
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Instructions */}
      <div className="absolute bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg max-w-sm text-sm text-gray-600">
        <div className="font-medium text-gray-800 mb-2">How to use:</div>
        <div>1. Start by describing your goal</div>
        <div>2. Chat with AI about your goal</div>
        <div>3. Branch with ⌘+Enter or the orange branch button</div>
        <div>4. Use menu button to access chat history</div>
        <div>5. Click collapsed workspaces to switch back</div>
      </div>
    </div>
  );
};

export default GoalStack;