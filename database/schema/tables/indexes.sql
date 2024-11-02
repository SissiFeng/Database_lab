-- Experiments 表索引
-- 时间相关索引（用于时序查询和监控）
CREATE INDEX idx_experiments_all_times ON experiments (
    planned_start_time,
    actual_start_time,
    actual_end_time
);
CREATE INDEX idx_experiments_status_time ON experiments (status, actual_start_time);

-- 状态和配置索引（用于实验监控和分析）
CREATE INDEX idx_experiments_status ON experiments (status);
CREATE INDEX idx_experiments_protocol ON experiments (protocol_version);
CREATE INDEX idx_experiments_config ON experiments USING gin (configuration);

-- Samples 表索引
-- 实验和样品关联索引
CREATE INDEX idx_samples_experiment_lookup ON samples (
    experiment_id,
    sample_code,
    status
);

-- 样品追踪索引
CREATE INDEX idx_samples_preparation ON samples (
    preparation_date,
    material_type,
    type
);

-- 样品关系索引（用于谱系追踪）
CREATE INDEX idx_samples_lineage ON samples (
    parent_sample_id,
    sample_id
);

-- 存储条件索引（用于库存管理）
CREATE INDEX idx_samples_storage ON samples (
    storage_location,
    status,
    expiration_date
);

-- 配置和条件索引
CREATE INDEX idx_samples_conditions ON samples USING gin (preparation_conditions);

-- Images 表索引
-- 实验和样品关联索引
CREATE INDEX idx_images_experiment_sample ON images (
    experiment_id,
    sample_id,
    image_type
);

-- 时间序列索引（用于时序分析）
CREATE INDEX idx_images_capture_timeline ON images (
    capture_time,
    device_id,
    image_type
);

-- 文件管理索引
CREATE INDEX idx_images_file_management ON images (
    file_path,
    file_format,
    quality_score
);

-- 设备参数索引
CREATE INDEX idx_images_device_settings ON images USING gin (device_settings);

-- Analysis Results 表索引
-- 实验和样品关联索引
CREATE INDEX idx_results_experiment_sample ON analysis_results (
    experiment_id,
    sample_id,
    analysis_type
);

-- 时间序列索引
CREATE INDEX idx_results_timeline ON analysis_results (
    started_at,
    completed_at,
    validation_status
);

-- 分析类型和版本索引
CREATE INDEX idx_results_analysis_type ON analysis_results (
    analysis_type,
    analysis_version,
    validation_status
);

-- 结果数据索引
CREATE INDEX idx_results_data ON analysis_results USING gin (result_data);

-- 部分索引（只为特定条件创建索引）
-- 只为有效的分析结果创建索引
CREATE INDEX idx_valid_results ON analysis_results (confidence_score)
WHERE is_valid = true;

-- 只为高质量图像创建索引
CREATE INDEX idx_high_quality_images ON images (image_id)
WHERE quality_score = 'excellent' OR quality_score = 'good';

-- 只为活跃实验创建索引
CREATE INDEX idx_active_experiments ON experiments (experiment_id)
WHERE status IN ('setup', 'running', 'paused');

-- 复合条件索引
CREATE INDEX idx_sample_monitoring ON samples (
    experiment_id,
    status,
    updated_at
) WHERE status IN ('in_analysis', 'prepared');