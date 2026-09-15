import React, { useState } from 'react';
import { UserCheck, X, AlertOctagon, CheckCircle2, MessageSquare, Send } from 'lucide-react';

interface HITLCorrectionModalProps {
  onClose: () => void;
}

export const HITLCorrectionModal: React.FC<HITLCorrectionModalProps> = ({ onClose }) => {
  const [feedbackType, setFeedbackType] = useState<'FALSE_POSITIVE' | 'FALSE_NEGATIVE' | 'BOUNDARY_CORRECTION'>('FALSE_POSITIVE');
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-mono select-none">
      <div className="w-full max-w-lg bg-[#0A101D] border border-cyber-cyan rounded-xl shadow-2xl p-6 relative space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
              HUMAN-IN-THE-LOOP ACTIVE LEARNING ANNOTATION
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {submitted ? (
          <div className="p-6 text-center space-y-3 bg-[#050811] rounded-lg border border-cyber-emerald">
            <CheckCircle2 className="w-10 h-10 text-cyber-emerald mx-auto animate-bounce" />
            <div className="text-sm font-bold text-slate-100 uppercase">ANNOTATION QUEUED FOR MODEL RETRAINING</div>
            <p className="text-xs text-slate-400">
              Domain expert correction logged. Feedback queued for active-learning gradient update.
            </p>
            <button
              onClick={onClose}
              className="mt-2 px-4 py-2 bg-cyber-cyan text-black font-bold text-xs rounded hover:bg-cyan-300 transition"
            >
              CLOSE
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div className="space-y-2">
              <label className="text-slate-400 font-bold uppercase">CORRECTION TYPE:</label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: 'FALSE_POSITIVE', label: 'FALSE POSITIVE' },
                  { id: 'FALSE_NEGATIVE', label: 'FALSE NEGATIVE' },
                  { id: 'BOUNDARY_CORRECTION', label: 'BOUNDARY MESH' }
                ].map((type) => (
                  <button
                    key={type.id}
                    type="button"
                    onClick={() => setFeedbackType(type.id as any)}
                    className={`py-2 rounded font-bold transition border ${
                      feedbackType === type.id
                        ? 'bg-cyber-cyan/20 text-cyber-cyan border-cyber-cyan shadow-cyan-glow'
                        : 'bg-[#050811] text-slate-400 border-slate-800 hover:border-slate-600'
                    }`}
                  >
                    {type.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-slate-400 font-bold uppercase">DOMAIN EXPERT NOTES:</label>
              <textarea
                rows={3}
                required
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="e.g. Mask captured seasonal agricultural harvesting instead of unauthorized building..."
                className="w-full bg-[#050811] border border-cyber-border rounded p-3 text-slate-100 placeholder-slate-500 focus:border-cyber-cyan focus:outline-none resize-none"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-cyber-cyan text-black font-bold text-xs rounded hover:bg-cyan-300 transition shadow-cyan-glow flex items-center justify-center gap-2"
            >
              <Send className="w-4 h-4" /> SUBMIT ANNOTATION TO ACTIVE LEARNING
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
