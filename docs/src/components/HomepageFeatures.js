import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Unified API',
    emoji: '🔌',
    description: (
      <>
        Single interface for reading and writing multiple data formats. Works with CSV, JSON, Parquet, XML, and 80+ more formats.
      </>
    ),
  },
  {
    title: 'Automatic Detection',
    emoji: '🔍',
    description: (
      <>
        Automatically detects file type and compression from filename. No need to specify format or codec manually.
      </>
    ),
  },
  {
    title: 'Preserves Nested Data',
    emoji: '📊',
    description: (
      <>
        Handles complex nested structures as Python dictionaries, unlike pandas DataFrames which require flattening.
      </>
    ),
  },
];

function Feature({emoji, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureEmoji}>{emoji}</div>
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
