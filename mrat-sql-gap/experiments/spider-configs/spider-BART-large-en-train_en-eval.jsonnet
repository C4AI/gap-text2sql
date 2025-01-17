{
    local exp_id = 1,
    logdir: "logdir/BART-large-en-train",
    model_config: "experiments/spider-configs/BART-large-en/gap-bart.jsonnet",
    model_config_args: {
        bs: 12,
        num_batch_accumulated: 2,
        bart_version: "facebook/bart-large",
		pretrained_checkpoint: "models/BART-large/pretrained_checkpoint/pytorch_model.bin",
        summarize_header: "avg",
        use_column_type: false,
        num_layers: 8,
        lr: 1e-4,
        bert_lr: 1e-5,
        att: 1,
        end_lr: 0,
        sc_link: true,
        cv_link: true,
        use_align_mat: true,
        use_align_loss: true,
        bart_token_type: true,
        decoder_hidden_size: 512,
        end_with_from: true, # equivalent to "SWGOIF" if true
        clause_order: null, # strings like "SWGOIF", it will be prioriotized over end_with_from 
    },

    eval_name: "bart-large-en_run_%d_%s_%d" % [exp_id, self.eval_use_heuristic, self.eval_beam_size],
    eval_output: "ie_dirs/BART-large-en-train_en-eval",
    eval_beam_size: 1,
    eval_use_heuristic: true,
    eval_steps: [40300],
    eval_section: "val",
}